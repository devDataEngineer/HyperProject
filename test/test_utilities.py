from utilities.utilities import format_extract_lambda_as_rows



def test_format_extract_lambda_as_rows_results_in_a_dictionary():
    rows_list = [["value1","value2","value3","value4"],
                ["value5","value6","value7","value8"],
                ["value9","value10","value11","value12"]]
    columns_list = ["column1","column2","column3","column4"]
    formatted_value = format_extract_lambda_as_rows(rows_list,columns_list)
    assert isinstance(formatted_value, list)

def test_format_extract_lambda_as_rows_assignes_correct_columns_to_every_row():
    rows_list = [["value1","value2","value3","value4"],
                  ["value5","value6","value7","value8"],
                   ["value9","value10","value11","value12"]]
    columns_list = ["column1","column2","column3","column4"]
    formatted_value = format_extract_lambda_as_rows(rows_list,columns_list)
    for item in formatted_value:
        for i,column in enumerate(item):
            assert column == columns_list[i]

def test_format_extract_lambda_as_rows_assignes_correct_values():
    rows_list = [["value1","value2","value3","value4"],
                  ["value5","value6","value7","value8"],
                   ["value9","value10","value11","value12"]]
    columns_list = ["column1","column2","column3","column4"]
    formatted_value = format_extract_lambda_as_rows(rows_list,columns_list)
    for j,item in enumerate(formatted_value):
        for i,column in enumerate(item):
            assert item[column] == rows_list[j][i]