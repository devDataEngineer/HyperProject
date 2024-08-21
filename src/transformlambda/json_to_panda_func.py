import pandas as pd
import json

def json_to_panda_df(json_file_path):
    
    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
        panda_df = pd.DataFrame(json_data)
        
        if panda_df.empty == True:
            return "The DataFrame is empty."
        else:
            return panda_df
    
    except FileNotFoundError:
        return "File not found."
    
    except json.JSONDecodeError:
        return "The file is not json."
    

    