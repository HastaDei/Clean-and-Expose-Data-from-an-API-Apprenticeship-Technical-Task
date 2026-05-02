# imports
from api_client import retrieve_raw_data
from storage import raw_data, working_data, clean_data, invalid_data
from processor import save_raw, normalise_field_names
from pprint import pprint


# get and store data
retrieved_data = retrieve_raw_data()
save_raw(retrieved_data)


# extract list from raw data
if isinstance(raw_data, list) and len(raw_data) > 0:
    working_data = raw_data[0].get("data", [])
else:
    working_data = []

# normalise data field names
working_data = normalise_field_names(working_data)

# test
pprint(raw_data)
pprint(f" THIS IS THE WORKING DATA {working_data}")
