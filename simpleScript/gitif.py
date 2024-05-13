"""
    generate ivanti to itop file (gitif) 
"""

import argparse
import sys
import shutil
import os

import pandas as pd


config_data = pd.DataFrame()


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

 
def get_heders_relation(config_file,itop_column, ivanti_column ):
    mapping_headers = {}
    for index, row in config_file.iterrows():
        if not pd.isna(row[ivanti_column]) and not pd.isna(row[itop_column]):  
            mapping_headers[row[ivanti_column]] = row[itop_column]
    return mapping_headers    


def process_input(args):
    if (args.configfile):
        print(args.configfile)
    if (args.file): 
        print(args.file)

def main():

    parser = argparse.ArgumentParser(description="Script para transformar una exportacion de itop a una importacion de ivanti")
    parser.add_argument("-c","--configfile", help="Archivo de configuracion",required=False)
    parser.add_argument("-f","--file", help="archivo de itop csv",required=False)
    parser.add_argument("-o","--output",help="salida de los archivos",required=False)
    parser.add_argument("-sf","--showformat", help="Ruta del archivo de configuración",required=False)

    args = parser.parse_args()

    if not (
        args.configfile or 
        args.file or 
        args.output or 
        args.showformat
    ):
        print("Debe proporcionar al menos un parametro")
        parser.print_help()
        sys.exit(1)
    else: 
        process_input(args)



if __name__ == "__main__":
    main()
