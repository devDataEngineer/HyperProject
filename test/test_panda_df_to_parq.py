import pandas as pd
from src.transformlambda.json_to_panda_func import json_to_panda_df
from src.transformlambda.panda_df_to_parq import convert_dataframe_to_parquet
from io import BytesIO

def test_func_returns_correct_return_string():
    df1 = json_to_panda_df("test/jsonpandatestfiles/test_json_panda_format_one.json")
    result = convert_dataframe_to_parquet(df1)
    assert isinstance(result, bytes)
    

def test_file_created_starts_with_correct_bytes():
    df1 = json_to_panda_df("test/jsonpandatestfiles/test_json_panda_format_one.json")
    result = convert_dataframe_to_parquet(df1)
    byte_string = str(bytearray(result))
    first_four_bytes = byte_string[10:16]
    assert first_four_bytes == "b'PAR1"

def test_file_created_ends_with_correct_bytes():
    df1 = json_to_panda_df("test/jsonpandatestfiles/test_json_panda_format_one.json")
    result = convert_dataframe_to_parquet(df1)
    byte_string = str(bytearray(result))
    final_four_bytes = byte_string[-6:-2]
    assert final_four_bytes == 'PAR1'
