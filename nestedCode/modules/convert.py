import pandas as pd

def create_ivanti_document(source_df: pd.DataFrame, headers_relation: dict ):
    export_document_df = pd.DataFrame()

    for column in headers_relation:
        if headers_relation[column] in source_df.columns :
            export_document_df[column] = source_df[headers_relation[column]]

    return export_document_df


def save_document(document: pd.DataFrame, fileName: str, route = "./output"):
    if route.endswith('/') or route.endswith('\\'):
        route = route[:-1]
    document.to_csv("{}/{}.csv".format(route,fileName),index=False)

    