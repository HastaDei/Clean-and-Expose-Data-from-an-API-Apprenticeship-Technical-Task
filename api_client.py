# imports
import requests
from config import API_URL, API_KEY


# define function for raw data retrieval
def retrieve_raw_data():
    # define headers
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    # make request
    response = requests.get(API_URL, headers=headers)

    # return data if request succeeds 
    if response.status_code == 200:
        return response.json()
    # raise error if request fails
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
