import json
from typing import List, Dict, Any
import re

class EntityExtractor:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def extract_entities(self, doc: str) -> Dict[str, List[str]]:
        prompt = self._create_prompt(doc) # doc is expected to be a string in json format (key-value pairs)
        response = self.llm_client.complete(prompt) if self.llm_client else self._fake_response() # response is expected to be json containing only persons and organisations
        return self._parse_response(response)

    def _create_prompt(self, doc: str) -> str: 
        return (
            f"Extract person and organisation entities from the following document:\n\n"
            f"{doc}\n\n"
            f"Output the result as a JSON object with two keys: 'persons' and 'organisations'.\n"
            f"Example output:\n"
            f"{{'persons': ['John Doe'], 'organisations': ['Acme Corp']}}"
        )

    def _parse_response(self, response: str) -> Dict[str, List[str]]:
        # Attempt to parse as JSON
        try:
            data = json.loads(response) #
            return self._validate_and_extract(data)
        except json.JSONDecodeError:
            print("Error: JSON decoding failed. Trying fallback approaches.")

        # Fallback: attempt to clean up and parse JSON
        cleaned_response = self._clean_json_string(response)
        try:
            data = json.loads(cleaned_response)
            return self._validate_and_extract(data)
        except json.JSONDecodeError:
            print("Error: JSON decoding failed after cleaning.")

        # Fallback: handle different casing
        try:
            data = json.loads(response.lower())
            return self._validate_and_extract(data)
        except json.JSONDecodeError:
            print("Error: JSON decoding failed even after lowercasing.")

        # Final fallback: return empty result
        return {"persons": [], "organisations": []}

    def _clean_json_string(self, json_string: str) -> str:
        # Remove any unwanted characters and attempt to clean the JSON string
        json_string = re.sub(
            r"[^\x00-\x7F]+", "", json_string
        )  # Remove non-ASCII characters
        json_string = re.sub(r"(\w+):", r'"\1":', json_string)  # Ensure keys are quoted
        return json_string

    def _validate_and_extract(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        personList = data.get("Persons", data.get("persons", [])) # Check for keys "persons" and "Persons"

        organisationsList = data.get(
            "organisations", data.get("Organisations", data.get("organizations", data.get("Organizations", []))) # Check for organisations, Organisations, organizations, Organizations
        )

        if not isinstance(personList, list):
            personList = []
        if not isinstance(organisationsList, list):
            organisationsList = []

        personList = [person for person in personList if isinstance(person, str)]

        organisationsList = [org for org in organisationsList if isinstance(org, str)]

        return {"persons": personList, "organisations": organisationsList}
    
    def _fake_response(self):
        return (
            """ {
                "Persons" : ["Maverick", "Name2"],
                "organisations" :  ["Xapien", "FasterPay"],
                "shoe brands" : ["nike"],
                "persons" : ["Maverick2", "Name3"]
            } """   
        )
