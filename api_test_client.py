# imports
import requests
import json

# url for api call
BASE_URL = "http://127.0.0.1:8000"

# get clean records from clean-records api
def get_cleaned_records():
    response = requests.get(f"{BASE_URL}/cleaned-records")
    response.raise_for_status()
    return response.json()

# get invalid records from invalid-records api
def get_invalid_records():
    response = requests.get(f"{BASE_URL}/invalid-records")
    response.raise_for_status()
    return response.json()

# print data to verify retrieval
def print_data():
    # clean data
    print("\n=== CLEANED RECORDS ===")
    print(json.dumps(get_cleaned_records(), indent=2))
    # invalid data
    print("\n=== INVALID RECORDS ===")
    print(json.dumps(get_invalid_records(), indent=2))

# run only when executed directly
if __name__ == "__main__":
    print_data()
