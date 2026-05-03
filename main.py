# imports
from api_client import retrieve_raw_data
from storage import raw_data, working_data, clean_data, incomplete_data
from processor import save_raw, normalise_field_names, clean_all_records, split_records
from pprint import pprint


# get and store data
retrieved_data = retrieve_raw_data()
save_raw(retrieved_data)


# extract list from raw data
if isinstance(raw_data, list) and len(raw_data) > 0:
    working_data = raw_data[0].get("data", [])
# make data 
else:
    working_data = []

# normalise data field names
working_data = normalise_field_names(working_data)
# clean records in working_data
working_data = clean_all_records(working_data)

# test
for record in working_data:
    print(record)

# validate and split data 
valid, invalid = split_records(working_data)

# add valid data to clean data list
clean_data.extend(valid)
# add invalid data to incomplete data list
incomplete_data.extend(invalid)

for record in clean_data:
    print(f"valid_data: {record}")

for record in incomplete_data:
    print(f"invalid_data: {record}")


