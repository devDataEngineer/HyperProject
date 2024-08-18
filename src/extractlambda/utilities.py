def format_extract_lambda_as_rows(rows_list, columns_list):
    """ Formatting output in list of dictionaries with seperate
        dictionaries representing rows of <column:value> pairs:

       [{'column1': 'value1', 'column2': 'value2'}, 
        {'column1': 'value3', 'column2': 'value4'}, 
        {'column1': 'value5', 'column2': 'value6}]
        """
    formatted = [dict(zip(columns_list,row)) for row in rows_list]
    return formatted

# def format_extract_lambda_as_columns(rows_list, columns_list):
#     """ Formatting output in list of dictionaries with a single dict
#         having <column_name:[list_of_values]> pairs:

#        {column1:['value1','value2'], column2:['value1','value2'], 
#        column3:['value1','value2']}
#         """
    
#     # TBD....