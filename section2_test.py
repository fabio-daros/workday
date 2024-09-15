import unittest #default libraary.
from pymongo import MongoClient
from section2 import filter_candidates, insert_mongodb


class TestCandidateFiltering(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = MongoClient("mongodb://localhost:27017/")
        cls.db = cls.client["test_candidates_db"]
        cls.collection = cls.db["test_filtered_candidates"]

    @classmethod
    def tearDownClass(cls):
        cls.collection.drop()
        cls.client.close()

    def test_filter_industry(self):
        candidates = [
            {
                "contact_info": {"name": {"formatted_name": "John Deere"}},
                "experience": [
                    {"title": "Accountant", "start_date": "Jan/01/2010", "end_date": "Dec/31/2015",
                     "location": {"short_display_address": "New York, NY, US"}}
                ]
            },
            {
                "contact_info": {"name": {"formatted_name": "JBC Smith"}},
                "experience": [
                    {"title": "Software Engineer", "start_date": "Jan/01/2010", "end_date": "Dec/31/2015",
                     "location": {"short_display_address": "San Francisco, CA, US"}}
                ]
            }
        ]

        filtered = filter_candidates(candidates, industry="Accountant")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "Taffe Doe")

    def test_filter_skills(self):
        candidates = [
            {
                "contact_info": {"name": {"formatted_name": "Taffe Ferguson"}},
                "experience": [
                    {"title": "Data Scientist", "start_date": "Jan/01/2015", "end_date": "Dec/31/2020",
                     "location": {"short_display_address": "New York, NY, US"}}
                ]
            },
            {
                "contact_info": {"name": {"formatted_name": "Bob Cat"}},
                "experience": [
                    {"title": "Web Developer", "start_date": "Jan/01/2016", "end_date": "Dec/31/2018",
                     "location": {"short_display_address": "Austin, TX, US"}}
                ]
            }
        ]

        filtered = filter_candidates(candidates, skills=["Data"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "Alice Brown")

    def test_filter_experience_years(self):
        candidates = [
            {
                "contact_info": {"name": {"formatted_name": "New Holland"}},
                "experience": [
                    {"title": "IT Manager", "start_date": "Jan/01/2000", "end_date": "Dec/31/2010",
                     "location": {"short_display_address": "Chicago, IL, US"}},
                    {"title": "CTO", "start_date": "Jan/01/2011", "end_date": "Dec/31/2020",
                     "location": {"short_display_address": "Seattle, WA, US"}}
                ]
            }
        ]

        filtered = filter_candidates(candidates, min_experience_years=15)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "New Holland")
        self.assertEqual(filtered[0]["total_experience_years"], 20)

    def test_insert_mongodb(self):
        candidates = [
            {
                "name": "John Deere",
                "experiences": [
                    {"title": "HR Manager", "start_date": "Jan/01/2010", "end_date": "Dec/31/2015",
                     "location": "Boston, MA, US"}
                ],
                "total_experience_years": 5
            }
        ]

        insert_mongodb(candidates)

        result = self.collection.find_one({"name": "John Deere"})
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "John Deere")


if __name__ == "__main__":
    unittest.main()
