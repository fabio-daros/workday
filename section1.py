import ssl #default libraary.
import json #default libraary.
import urllib.request #default libraary.
from datetime import datetime #default libraary.

url = "https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json"
ssl_context = ssl._create_unverified_context()


def get_candidates(url):
    try:
        with urllib.request.urlopen(url, context=ssl_context) as response:
            if response.status == 200:
                data = response.read()
                return json.loads(data)
            else:
                raise Exception(f"Error to get data: {response.status}")
    except Exception as e:
        print(f"An error occurred: {e}")


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b/%d/%Y")
    except ValueError:
        return None


def calculate_gap(end_date, start_date):
    previous_end = parse_date(end_date)
    next_start = parse_date(start_date)
    if previous_end and next_start:
        gap_days = (next_start - previous_end).days

        return max(gap_days, 0)
    return 0


def format_print(experience, previous_end_date):
    title = experience.get("title")
    start_date = experience.get("start_date")
    end_date = experience.get("end_date")
    location = experience.get("location", {}).get("short_display_address", "Unknown")

    gap_days = calculate_gap(previous_end_date, start_date) if previous_end_date else 0

    gap_message = f" Gap in CV for {gap_days} days" if gap_days > 0 else ""

    return f"Worked as: {title}, From {start_date} To {end_date} in {location}\n{gap_message}"


def print_candidates(candidate):
    name = candidate.get("contact_info", {}).get("name", {}).get("formatted_name", "Unknown")
    print()
    print(f"Hello {name},")

    experience_list = candidate.get("experience", [])
    if not experience_list:
        print("No experience found.")
        return

    previous_end_date = None
    for experience in experience_list:
        print(format_print(experience, previous_end_date))
        previous_end_date = experience.get("end_date")


def main():
    candidates = get_candidates(url)
    if not candidates:
        print("No candidates found")
        return

    for candidate in candidates:
        print_candidates(candidate)


if __name__ == "__main__":
    main()
