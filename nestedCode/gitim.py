
import argparse
import shutil
import os

import pandas as pd
import modules.headers as hdrs
import modules.convert as cvrt

def procesar_archivos(ruta_configuracion):

    try:
        conf_df = pd.read_csv(ruta_configuracion, index_col=False, encoding='latin-1', low_memory=False) 
    except FileNotFoundError:
        print("No se encontro el archivo '{ruta_configuracion}'")

    try:
        incident_df = pd.read_csv('./files/Incident/Incidente Exportar.csv', index_col=False, encoding='latin-1', low_memory=False) 

        mapping_incident = hdrs.get_heders_relation(conf_df,'ITOP-INCIDENT','IVANTI')
        
        export_incident_doc = cvrt.create_ivanti_document(incident_df,mapping_incident)

        cvrt.save_document(export_incident_doc,'ivanti_incident')

        print("incident_doc creado")
    except FileNotFoundError:
        print("No se encontro archivo de Incidente a convertir")


    try:
        request_df = pd.read_csv('./files/Request/Requerimiento Exportar.csv', index_col=False, encoding='latin-1', low_memory=False) 

        mapping_request = hdrs.get_heders_relation(conf_df,'ITOP-REQUEST','IVANTI')
        export_request_doc = cvrt.create_ivanti_document(request_df,mapping_request)

        cvrt.save_document(export_request_doc,'ivanti_request')

        print("request_doc creado")

    except FileNotFoundError:
        print("No se encontro archivo de UserRequest a convertir")
def main():

    parser = argparse.ArgumentParser(description="Procesar archivos según la configuración")
    parser.add_argument("config_route", help="Ruta del archivo de configuración")
    # parser.add_argument("origen", help="Ruta del archivo de origen")
    # parser.add_argument("salida", help="Nombre del archivo de salida")

    args = parser.parse_args()
    for ruta_archivo in [args.config_route]:
        if not os.path.exists(ruta_archivo):
            print(f"Error: La ruta del archivo '{ruta_archivo}' no existe.")
            return

    # Procesar los archivos
    procesar_archivos(args.config_route)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        # print("Usage: python gitm.py <config_file> <source_itop_file> <output_dir>")
        print("Usage: python gitm.py <config_file>")

    else:
        main()
