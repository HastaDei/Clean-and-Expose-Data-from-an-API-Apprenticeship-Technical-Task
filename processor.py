# imports
from api_client import retrieve_raw_data
from storage import raw_data, working_data, clean_data, invalid_data


# save raw data function
def save_raw(data):
    raw_data.append(data)
    working_data.append(data)
