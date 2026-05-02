# imports
from api_client import retrieve_raw_data
from storage import raw_data, working_data, clean_data, invalid_data
from processor import save_raw


# get and save data
retrieved_data = retrieve_raw_data()
save_raw(retrieved_data)

print(f"This is the raw data: {raw_data}")
print(f"This is the working data: {working_data}")
