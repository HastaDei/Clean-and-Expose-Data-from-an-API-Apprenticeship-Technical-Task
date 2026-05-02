# imports
import re

from api_client import retrieve_raw_data
from storage import raw_data, working_data, clean_data, invalid_data


# save raw data function
def save_raw(data):
    raw_data.append(data)


# standardise field names function
def normalise_field(field:str) -> str:
    # convert to snake case
    field = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', field)

    # separate words with underscore
    field = re.sub(r'[\s\-]+', '_', field)

    # return field
    return field.lower().strip()

# map field names 
FIELD_NAME_MAP = {
    "id": "id",
    "first_name": "first_name",
    "firstname": "first_name",
    "last_name": "last_name",
    "lastname": "last_name",
    "email": "email",
    "phone": "phone",
    "start_date": "start_date",
    "startdate": "start_date",
    "active": "active",
    "course": "course",
}

# normalise whole dictionary function
def normalise_record(record: dict) -> dict:
    # define normalised dictionary
    normalised = {}

    # apply normalisation to all fields in record
    for field, value in record.items():
        normal_field = normalise_field(field)
        final_field = FIELD_NAME_MAP.get(normal_field)
        
        # test
        print(final_field)

        # assign normalised value to dictionary
        if final_field:
            normalised[final_field] = value

    # return dictionary
    return normalised

# apply to whole list of dictionaries function
def normalise_field_names(data: list[dict]) -> list[dict]:
    return [normalise_record(record) for record in data]
