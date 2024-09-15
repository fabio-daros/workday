import ssl #default libraary.
import json #default libraary.
import logging #default libraary.
import urllib.request #default libraary.
from datetime import datetime #default libraary.
from pymongo import MongoClient


url = "https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json"
ssl_context = ssl._create_unverified_context()

# logging (default library)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("candidate_filter.log"),
        logging.StreamHandler()
    ]
)


def get_candidates(url):
    # Gets candidates from the URL.
    try:
        with urllib.request.urlopen(url, context=ssl_context) as response:
            if response.status == 200:
                data = response.read()
                logging.info("Data obtained successfully! ")
                return json.loads(data)
            else:
                raise Exception(f"Error to get data: {response.status}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b/%d/%Y")
    except ValueError:
        logging.warning(f"Invalid format {date_str}")
        return None


def calculate_experience(experience_list):
    total_days = 0
    for exp in experience_list:
        start_date = parse_date(exp.get("start_date"))
        end_date = parse_date(exp.get("end_date"))
        if start_date and end_date:
            total_days += (end_date - start_date).days
    return total_days / 365  # Return years of experience.


def filter_candidates(candidates, industry=None, skills=None, min_experience_years=None):
    filtered_candidates = []
    for candidate in candidates:
        name = candidate.get("contact_info", {}).get("name", {}).get("formatted_name", "Unknown")
        experience_list = candidate.get("experience", [])

        if not experience_list:
            logging.info(f"Candidate {name} do not have experience registered.")
            continue

        # filter sector
        if industry:
            if not any(industry.lower() in exp.get("title", "").lower() for exp in experience_list):
                logging.info(f"Candidate {name} do not stay in this sector.")
                continue

        # filter skills
        if skills:
            candidate_skills = set(candidate.get("skills", []))
            if not set(skills).issubset(candidate_skills):
                logging.info(f"Candidate {name} do not have the abilities: {skills}")
                continue

        # filter minimum years of experience
        if min_experience_years:
            total_experience_years = calculate_experience(experience_list)
            if total_experience_years < min_experience_years:
                logging.info(f"Candidate {name} do not have the years necessary")
                continue

        filtered_candidates.append({
            "name": name,
            "experiences": experience_list,
            "total_experience_years": calculate_experience(experience_list)
        })

        logging.info(f"Candidate {name} meets the criteria and was included ")

    return filtered_candidates


def insert_mongodb(candidates, db_name="candidates_db", collection_name="filtered_candidates"):
    # Inserts in a MongoDB.

    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(candidates)
    print(
        f"{len(candidates)} candidates were added to the collection '{collection_name}' from the database '{db_name}'.")


def main():
    # Requests user input for filtering criteria
    industry = input("Enter the industry: ")
    skills_input = input("Enter the required skills, separated by commas: ")
    min_experience_years = input("Enter the minimum number of years of experience: ")

    # Processes user input
    skills = [skill.strip() for skill in skills_input.split(',')] if skills_input else None
    min_experience_years = int(min_experience_years) if min_experience_years else None

    logging.info("Starting filtering.")

    # Gets candidate data
    candidates = get_candidates(url)
    if not candidates:
        logging.error("No candidates found.")
        return

    filtered_candidates = filter_candidates(
        candidates,
        industry=industry,
        skills=skills,
        min_experience_years=min_experience_years
    )

    if filtered_candidates:
        # Inserts candidates in MongoDB
        insert_mongodb(filtered_candidates)
    else:
        logging.info("No candidate meets the specified criteria.")


if __name__ == "__main__":
    main()
