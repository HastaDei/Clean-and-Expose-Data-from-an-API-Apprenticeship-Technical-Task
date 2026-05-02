# imports
import re
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from titlecase import titlecase

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
        # assign normalised value to dictionary
        if final_field:
            normalised[final_field] = value
    # return dictionary
    return normalised

# apply to whole list of dictionaries function
def normalise_field_names(data: list[dict]) -> list[dict]:
    return [normalise_record(record) for record in data]


# clean id function
def clean_id(value) -> str:
    # return nothing if value is blank or missing
    if value is None or str(value).strip() == "":
        return ""
    # keep as string and remove whitespace from ends
    return str(value).strip()

# clean name function
def clean_name(value: str) -> str:
    # return nothing if value is blank or missing
    if value is None or str(value).strip() == "":
        return ""
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
        return ""
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
        return ""
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
        return ""
    # keep as string and remove whitespace from ends
    date_str = str(date_str).strip()
    # normalise separators
    date_str = date_str.replace(".", "/").replace("-", "/")
    # convert to iso format if possible
    for fmt in ("%d/%m/%Y", "%Y/%m/%d"):
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
    if value is None or str(value).strip() == "":
        return ""
    # keep as string, remove whitespace from ends, and make lowercase
    value = str(value).strip().lower()
    # return bool value
    return value in ("true", "1", "yes", "y", "active")

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
