# **Clean-and-Expose-Data-from-an-API-Apprenticeship-Technical-Task**
## **How to run:**
### <ins>Initial Setup</ins>

- In the terminal run "**pip install -r requirements.txt**".
- Use the .env.example as a template to create a .env file. \
Replace "**url**" with a valid API url and "**key**" with a valid API key inside the .env file.

### <ins>Running Order</ins>

- Running the main.py file will automatically fetch the API data and attempt to clean it. \
Cleaned and incomplete data can be found in the clean.json and invalid.json files after running main.py. \
**Note**, due to the API returning randomized test data, some runs may yield no valid records under strict validation rules. Strict validation criteria intentionally prioritise data integrity over volume, which may result in a lower proportion of accepted records. In the event that the clean.json file is empty, or the API test returns an empty list, and clean data is required for testing purposes, please run main.py again to receive records that meet the validation criteria.

- Start the API server endpoints by running "**uvicorn server.api_server:app --reload**" in the terminal. \
The API will start running and the response models can be viewed at "http://127.0.0.1:8000/docs". \
To stop the API from running, press "**CTRL + C**" in the terminal from which the API was started.

- To test the ability of fetching data from the API endpoints, you can run the included api_test_client.py file inside utils. \
You can do so by typing "**python utils\api_test_client.py**" inside the terminal. \
**Note**, you may need to use a second terminal for this while the API is running. 
    - To test the API endpoints separately you can do so using these urls: \
    Cleaned records "http://127.0.0.1:8000/cleaned-records" \
    Invalid records "http://127.0.0.1:8000/invalid-records"
---
## **Assumptions and Improvements:** 
### <ins>Fetching Raw Data from API</ins>

- The main pipeline calls the external client API function to fetch the raw data and store it in a list called raw_data.  \
This is then transferred to a working_data list in which data is meant to be cleaned and validated.

- The retrieved data is wrapped using the envelope pattern, so transferring from raw_data to working_data requires extractions from the outer layer. 

- **The assumption** made is that all API calls will retrieve the exact same API response structure. (This assumption is scoped to the controlled test API provided for the task.)

- **To improve** data retrieval robustness, the extraction process would need to be redesigned to accept common API response patterns. The current implementation only avoids crashing by returning an empty working_data list when the extraction fails.

### <ins>Normalising Field Names</ins>

- The field names are normalised for all records in the working_data list of dictionaries. \
The functions for field name normalisation can silently drop unrecognised fields but do not add missing fields. \
All original data is preserved in raw_data for the program lifecycle; transformations only apply to derived datasets.

- **The assumption** made is that all retrieved data sets will have no additional or missing fields.

- **To improve** field name normalisation, the functions should be designed to detect and add missing fields. \
Additionally, the functions should not silently drop any unrecognised fields. \
The current implementation attempts to clean messy field names but fails to enforce a consistent dataset structure.

### <ins>Cleaning Records</ins>

- Records are cleaned using functions by converting the field values into strings (except for the "active" field which is converted to a boolean). 
    - The strings are stripped of unnecessary spaces and structured according to their field types. This approach ensures consistency for JSON serialization, though internal type handling (e.g., datetime objects) could improve robustness. 
    - Names and courses are capitalised, emails are kept lower case, phone numbers are converted to follow the E.164 format, and dates are converted to follow the ISO 8601 format. 
    - Values that cannot be successfully cleaned are left unchanged, except missing or empty values, which are set to None. 
    
    <br> 

- **The assumption** made for cleaning ID values is that they should not be converted to integers, due to unknown database storage type requirements, and as a result they were kept as strings. The values with missing leading 0s were normalised to a 3-character format based on observed consistency in the dataset. This **assumption** operates on the basis of maintaining as much of the original data as possible, while normalising the values to help with the verification of duplicate records. 

- **The assumption** made for cleaning name values is that all names contain a single capital letter at the start. As a result, names with apostrophes or internal capitals, will not be assigned the additional capital letter. \
**To improve** the name cleaning function, additional libraries and techniques could be employed to handle the complexity of human names without losing essential formatting.

- **The assumption** made for cleaning email values is that incomplete or misconfigured values should not be presumed or deduced based on popular expectations. While the ability to estimate domain extensions or to replace missing symbols, such as "@" and ".", is there, the resulting data would not be guaranteed to be correct as you cannot infer user and domain names with 100% accuracy.

- **The assumption** made for cleaning date values is that the original date formats are following European standards. Date parsing uses heuristic ordering based on common formats due to lack of explicit specification. Consequently, the date formats can be converted to ISO, but it is not possible to determine the original format of the date and confirm the validity of the change with 100% accuracy. 

- **The assumption** made for active status values is that the options are limited to only true or false, and are meant to be stored as boolean values. 


### <ins>Validating Records</ins>

- **The assumption** made for validating records is that no field in any record should have missing or misconfigured values. \
With no information on which fields may be optional, the decision was made that only records with all 8 correctly structured values present would be considered clean. Records missing any of the required 8 fields are classified as invalid to meet task requirements.

### <ins>Global Improvements</ins>

- **To improve** the ability to run the project, the application startup initialisation could be refined and reconfigured to automatically run the API and data processing pipeline. The implementation would have a startup initialisation step that runs the data pipeline before exposing the API.

- **To improve** the data handling and storage, the current implementation should be modified to avoid relying on static json files for providing the API endpoints with access to the data. The reconfiguration would have better implemented memory storage alternatives for exclusive management of data in memory, or it could include a database in which data may be stored for improved effectiveness and security. 

- **To improve** consistency and usability of data sharing through API endpoints, responses should be wrapped in a standard API response structure instead of being returned in a basic, unstructured format.