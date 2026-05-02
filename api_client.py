# imports
import requests
from config import API_URL, API_KEY


# defining function for raw data retrieval
def retrieve_raw_data():
    # defining headers
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    # making request
    response = requests.get(API_URL, headers=headers)

    # returning data if request succeeds 
    if response.status_code == 200:
        return response.json()
    # raising error if request fails
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")


# testing function
test_run = retrieve_raw_data()
print(test_run)
