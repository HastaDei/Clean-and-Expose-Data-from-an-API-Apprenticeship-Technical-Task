# imports
from api_client import retrieve_raw_data
from storage import raw_data, working_data
from processor import save_raw, normalise_field_names, clean_all_records, split_records, save_valid, save_invalid


def run_main_pipeline():

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

    # save data
    save_valid(valid)
    save_invalid(invalid)

    # test
    for record in valid:
        print(f"valid_data: {record}")
    for record in invalid:
        print(f"invalid_data: {record}")

run_main_pipeline()
