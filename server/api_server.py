# imports
from fastapi import FastAPI

from server.models import CleanRecord, InvalidRecord
from processor import get_cleaned, get_invalid


# create application instance
app = FastAPI()

# endpoint for cleaned records
@app.get("/cleaned-records", response_model=list[CleanRecord])
def cleaned_records():
    # return copy of cleaned data
    return get_cleaned().copy()

# endpoint for invalid records
@app.get("/invalid-records", response_model=list[InvalidRecord])
def invalid_records():
    # return copy of invalid data
    return get_invalid().copy()
