import pandas as pd


def create_df_dim_design(df_design):
       
    dim_design = df_design
    dim_design = dim_design.drop(columns=['created_at', 'last_updated'])
    dim_design.set_index = dim_design['design_id']
    dim_design.name = "dim_design"
    return dim_design
   
    