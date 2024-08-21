from src.transformlambda.json_to_panda_func import json_to_panda_df
import pandas as pd

def test_returns_panda_df():
    json_file_one_table = "test/jsonpandatestfiles/test_json_panda_format_one.json"
    result = json_to_panda_df(json_file_one_table)
    assert isinstance(result, pd.DataFrame)

def test_empty_json_as_arg():
    json_file_empty = "test/jsonpandatestfiles/test_json_panda_empty.json"
    result = json_to_panda_df(json_file_empty)
    assert result == "The DataFrame is empty."

def test_non_json_file_arg():
    non_json_file = "test/jsonpandatestfiles/python_dummy_func.py"
    result = json_to_panda_df(non_json_file) 
    assert result == "The file is not json."

def test_file_not_found_arg():
    result = json_to_panda_df("dont_exist.json")
    assert result == "File not found."