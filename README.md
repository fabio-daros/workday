# Candidate Filtering Script

## Description

This is a Python script that does the following:
1. Gets candidate data from URL: "https://hs-recruiting-test-resume-data.s3.amazonaws.com/allcands-full-api_hub_b1f6-acde48001122.json."
2. Filters candidates based on specific criteria (industry, skills, and minimum years of experience).
3. Insert the filtered data into a MongoDB collection called `filtered_candidates`.

## Requirements

- Python 3.x
- Python libraries: `pymongo`, `urllib`, `json`, `ssl`
- MongoDB running locally

## Installation

1. **Install the required libraries**:

   ```bash
   pip3 install pymongo
   
2. To execute the script, run the following command:

   ```bash
   python3 section2.py
   ```
