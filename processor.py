# imports
import re
import json
import phonenumbers
from datetime import datetime
from titlecase import titlecase
from collections import defaultdict

from storage import raw_data


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
        # assign normalised value to dictionary
        if final_field:
            normalised[final_field] = value
    # return dictionary
    return normalised

# apply to whole list of dictionaries function
def normalise_field_names(data: list[dict]) -> list[dict]:
    return [normalise_record(record) for record in data]


# clean id function
def clean_id(value, length: int = 3) -> str:
    # return nothing if value is blank or missing
    if value is None or str(value).strip() == "":
        return None
    # keep as string and remove whitespace from ends
    value = str(value).strip()
    # return value with leading 0s to fit length requirements
    return value.zfill(length)

# clean name function
def clean_name(value: str) -> str:
    # return nothing if value is blank or missing
    if value is None or str(value).strip() == "":
        return None
    # keep as string, remove whitespace from ends, and make lowercase
    value = str(value).strip().lower()
    # collapse multiple spaces inside name
    value = re.sub(r"\s+", " ", value)
    # return value with title case
    return titlecase(value)

# clean email function
def clean_email(email: str) -> str:
    # return nothing if email is blank or missing
    if email is None or str(email).strip() == "":
        return None
    # keep as string, remove whitespace from ends, and make lowercase
    email = str(email).strip().lower()
    # remove all spaces in the email address
    email = re.sub(r"\s+", "", email)
    # return email
    return email

# clean phone number function
def clean_phone(phone: str, region="GB") -> str:
    # return nothing if phone is blank or missing
    if phone is None or str(phone).strip() == "":
        return None
    # keep as string and remove whitespace from ends
    phone = str(phone).strip()
    # remove unwanted characters but keep + if present
    phone = re.sub(r"[^\d+]", "", phone)
    # parse to E164 format
    try:
        parsed = phonenumbers.parse(phone, region)
        # return parsed phone number
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except:
        # return phone number if unable to parse
        return phone

# clean date function
def clean_date(date_str: str) -> str:
    # return nothing if date is blank or missing
    if date_str is None or str(date_str).strip() == "":
        return None
    # keep as string and remove whitespace from ends
    date_str = str(date_str).strip()
    # normalise separators
    date_str = date_str.replace(".", "/").replace("-", "/")
    # convert to iso format if possible
    for fmt in ("%d/%m/%Y", "%Y/%m/%d", "%Y/%d/%m", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date().isoformat()
        # continue if unable to parse
        except ValueError:
            continue
    # return date if unable to parse
    return date_str

# clean activity function
def clean_activity(value) -> bool:
    # return boolean value if already boolean
    if isinstance(value, bool):
        return value
    # return nothing if value is blank or missing
    elif value is None or str(value).strip() == "":
        return None
    # keep as string, remove whitespace from ends, and make lowercase
    value = str(value).strip().lower()
    # return true if value matchhes
    if value in ("true", "1", "yes", "y", "active"):
        return True
    # return false if value matches
    elif value in ("false", "0", "no", "n"):
        return False
    # return initial value if unable to match to boolean value
    return value

# clean record (dictionary) function
def clean_record(record: dict) -> dict:
    # return dictionary of records after cleaning attempt
    return {
        "id": clean_id(record.get("id")),
        "first_name": clean_name(record.get("first_name")),
        "last_name": clean_name(record.get("last_name")),
        "email": clean_email(record.get("email")),
        "phone": clean_phone(record.get("phone")),
        "start_date": clean_date(record.get("start_date")),
        "active": clean_activity(record.get("active")),
        "course": clean_name(record.get("course")),
    }

# clean list of records (dictionaries) function
def clean_all_records(records: list[dict]) -> list[dict]:
    # return records after cleaning attempt
    return [clean_record(r) for r in records]


# check if value is missing function
def is_missing(value) -> bool:
    # true if no value
    if value is None:
        print(f"{value} is_missing TRUE")
        return True
    # true if value is blank
    elif isinstance(value, str) and value.strip() == "":
        print(f"{value} is_missing TRUE")
        return True
    # return false if value is not missing
    print(f"{value} is_missing FALSE")
    return False

# verify if value is missing in dictionary function
def validate_missing(record: dict) -> bool:
    # return validation result
    return not any(is_missing(v) for v in record.values())

# email structure
EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
# validate email function
def validate_email_address(email: str) -> bool:
    # return true if email follows regex structure
    if isinstance(email, str) and re.match(EMAIL_REGEX, email) is not None:
        print(f"VALID EMAIL, {email}")
        return True
    # return false if email doesn't follow regex structure
    else:
        print(f"INVALID EMAIL, '{email}'")
        return False

# phone structure
PHONE_REGEX = r"^\+?\d{10,15}$"
# validate phone number function  
def validate_phone(phone: str, region="GB") -> bool:
    # return true if phone number follows regex structure
    if isinstance(phone, str) and re.match(PHONE_REGEX, phone) is not None:
        print(f"VALID PHONE {phone}")
        return True
    # return false if phone number doesn't follow regex structure
    else:
        print(f"INVALID PHONE {phone}")
        return False
    
# validate date function
def validate_date(date_value: str) -> bool:
    # return true if date is confirmed iso format
    try:
        datetime.fromisoformat(date_value)
        print(f"VALID DATE {date_value}")
        return True
    # return false if date confirmation fails
    except:
        print(f"INVALID DATE {date_value}")
        return False
    
# check if boolean function
def validate_activity(activity: bool) -> bool:
    print(f"activity : {activity}")
    # return true if boolean or false if not
    return isinstance(activity, bool)

# group dictionaries with the same id function
def group_by_id(records):
    groups = defaultdict(list)
    # loop for appending records
    for record in records:
        groups[record.get("id")].append(record)
    # returning dictionary of lists of dictionaries
    return groups

# function to verify duplicate records
def validate_duplicates(records):
    # call function to group records
    groups = group_by_id(records)
    # define temporary lists for unique records and duplicate records
    valid_records = []
    invalid_records = []
    # loop through each id and record sharing the id
    for record_id, group in groups.items():
        # continue if group contains no duplicates
        if len(group) == 1:
            valid_records.append(group[0])
            continue
        # identify first apearance of id and subsequent appearances 
        first = group[0]
        rest = group[1:]
        # check if duplicate records have identical names
        for record in rest:
            same_name = (record.get("first_name") == first.get("first_name") and
                record.get("last_name") == first.get("last_name"))
            # invalidate subsequent records with identical id and names
            if same_name:
                invalid_records.append(record)
            # invalidate both records if duplicate id but names don't match
            else:
                invalid_records.append(first)
                invalid_records.append(record)
        # confirm id is not in the invalid list before validating
        if first not in invalid_records:
            valid_records.append(first)
    # return lists of valid and invalid records
    return valid_records, invalid_records

# call validation functions to validate record function
def validate_record(record: dict) -> dict:
    # hold validation boolean values in list
    validation_results = [
        validate_missing(record),
        validate_email_address(record.get("email")),
        validate_phone(record.get("phone")),
        validate_date(record.get("start_date")),
        validate_activity(record.get("active"))
    ]
    # check if validation returns any false values
    print(validation_results)
    print()
    if False in validation_results:
        return False
    elif all(validation_results):
        return True

# separate clean data from invalid data function
def split_records(records):
    # define valid and invalid lists
    valid = []
    invalid = []
    for record in records:
        # append validated record to the clean_data list
        if validate_record(record):
            valid.append(record)
        # append records with failed validation to the invalid_data list
        else:
            invalid.append(record)
    # check for duplicate valid data
    valid, dup_invalid = validate_duplicates(valid)
    # add duplicate records to invalid list
    if len(dup_invalid) > 0:
        invalid.extend(dup_invalid)
    # returning valid and invalid lists
    return valid, invalid



# write clean data to json file
def save_valid(valid):
    with open("clean.json", "w") as f:
        json.dump(valid, f)

# write invalid data to json file
def save_invalid(invalid):
    with open("invalid.json", "w") as f:
        json.dump(invalid, f)

# fetch clean data function
def get_cleaned():
    # open and return data from file
    with open("clean.json", "r") as f:
        return json.load(f)

# fetch invalid data function
def get_invalid():
    # open and return data from file
    with open("invalid.json", "r") as f:
        return json.load(f)
