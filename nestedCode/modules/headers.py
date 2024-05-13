import pandas as pd
def get_heders_relation(config_file,itop_column, ivanti_column ):
    mapping_headers = {}
    for index, row in config_file.iterrows():
        if not pd.isna(row[ivanti_column]) and not pd.isna(row[itop_column]):  
            mapping_headers[row[ivanti_column]] = row[itop_column]
    return mapping_headers    

