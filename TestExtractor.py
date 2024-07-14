import pytest
from EntityExtractor import EntityExtractor

# ------------------------------------- Start of response format checks -------------------------------------

def test_response_is_empty(): 
    extractor = EntityExtractor();
    response = '{}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": [], "organisations": []}
    assert result == expectedResult, "Failed to parse empty response."

def test_response_contains_entities(): 
    extractor = EntityExtractor();
    response = '{"persons": ["Maverick", "Name2"], "organisations": ["Xapien", "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "Name2"], "organisations": ["Xapien", "FasterPay"]}
    assert result == expectedResult, "Failed to parse response containing entities."

def test_response_contains_duplicate_entity_keys(): 
    extractor = EntityExtractor();
    response = '{"persons" : ["Maverick", "Name2"], "persons" : ["Maverick2", "Name3"], "organisations": ["Xapien", "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "Name2", "Maverick2", "Name3"], "organisations": []}
    assert result == expectedResult, "Failed to parse response containing duplicate entity keys."

def test_response_contains_irrelevant_keys(): 
    extractor = EntityExtractor();
    response = '{"persons" : ["Maverick", "Name2"], "organisations": ["Xapien", "FasterPay"], "shoe brands": ["Nike", "Adidas"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "Name2"], "organisations": ["Xapien", "FasterPay"]}
    assert result == expectedResult, "Failed to parse response containing irrelevant entity keys."

def test_response_contains_nested_entity_keys(): 
    extractor = EntityExtractor();
    response = '{"information" { "persons": [ "Maverick", "Name2"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "Name2"], "organisations": []}
    assert result == expectedResult, "Failed to parse response containing nested entity keys."

# ------------------------------------- Start of key / value checks -------------------------------------

def test_values_not_contained_in_list(): 
    extractor = EntityExtractor(); 
    response = '{"persons": "Maverick", "organisations": "Xapien"}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick"], "organisations": ["Xapien"]}
    assert result == expectedResult, "Failed to parse response containing values not in a list."

def test_remove_non_ASCII_characters(): 
    extractor = EntityExtractor();
    response = '{"persons": ["Maverick", "\u4F60\u597D"], "organisations": ["Xapien", "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", ""], "organisations": ["Xapien","FasterPay"]}
    assert result == expectedResult, "Failed to remove non-ASCII characters"

def test_uppercase_keys(): 
    extractor = EntityExtractor();
    response = '{"PERSONS": ["Maverick", "Name2"], "ORGANISATIONS": ["Xapien", "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "Name2"], "organisations": ["Xapien", "FasterPay"]}
    assert result == expectedResult, "Failed to parse response containing uppercase entity keys."

def test_ensure_values_are_quoted():
    extractor = EntityExtractor();
    response = '{"persons": [Maverick, "name2"], "organisations": [Xapien, "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "name2"], "organisations": ["Xapien","FasterPay"]}
    assert result == expectedResult, "Failed to parse response containing unquoted values"

def test_ensure_keys_are_quoted():
    extractor = EntityExtractor();
    response = '{persons: ["Maverick", "name2"], organisations: ["Xapien", "FasterPay"]}'
    result = extractor._parse_response(response)
    expectedResult = {"persons": ["Maverick", "name2"], "organisations": ["Xapien","FasterPay"]}
    assert result == expectedResult, "Failed to parse response containing unquoted keys"


if __name__ == "__main__":
    pytest.main()