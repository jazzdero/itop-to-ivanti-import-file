"""
    generate ivanti to itop file (gitif) 

    to gen .exe > pyinstaller --onefile .\gitif.py
"""

import argparse
import sys
import json

import pandas as pd

filename = ''
output_route = './'

config_data = {
    'incident'  : {
        'client_id' : "D82B5035AFEA40A883E455FBB61D0227",
        'prfile_id' : "89E90F1C3492462385A1AF8BDB43D59A",
        'LoginId' : "usuario.asf",
        'OwningOrgUnitId' : 'OFI PC',
        'Owner' : 'Usuario Mesa de Servicio',
        'Service' : 'Servicio de arrendamiento de equipo de computo',
        'Category': 'Calentamiento del equipo',
        'OrganizationUnitID' : 'ASF - Auditoría Superior de la Federación',
        'Email' : 'asf@test.com',
        'ProfileFullName' : 'Cliente ASF',
        'fields'  :  [{
                'en_itop' : [''],
                'es_itop' : ['Id (Clave Primaria)'],
                'ivanti'  : 'RecId',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Organización->Nombre'],
                'ivanti'  : 'zClient',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Asunto'],
                'ivanti'  : 'Subject',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Descripción'],
                'ivanti'  : 'Symptom',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Urgencia'],
                'ivanti'  : 'Urgency',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Impacto'],
                'ivanti'  : 'Impact',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Origen'],
                'ivanti'  : 'Source',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Prioridad'],
                'ivanti'  : 'Priority',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Analista->Nombre común'],
                'ivanti'  : 'zUsuarioFalla',
                'require_catalog' : False
            },]
    },
    'servicerequest'  : {
        'client_id' : "D82B5035AFEA40A883E455FBB61D0227",
        'LoginId' : "usuario.asf",
        'Service' : 'Servicio de Centro de Datos',
        'Owner' : 'Martin Juarez',
        'OrganizationUnitID' : 'ASF - Auditoría Superior de la Federación',
        'Email' : 'asf@test.com',
        'ProfileFullName' : 'Cliente ASF',
        'fields'  :  [{
                'en_itop' : [''],
                'es_itop' : ['Id (Clave Primaria)'],
                'ivanti'  : 'RecId',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Organización->Nombre'],
                'ivanti'  : 'zClientR',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Asunto'],
                'ivanti'  : 'Subject',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Descripción'],
                'ivanti'  : 'Symptom',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Subcategoría->Nombre'],
                'ivanti'  : 'zCategoria',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Urgencia'],
                'ivanti'  : 'Urgency',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Origen'],
                'ivanti'  : 'Source',
                'require_catalog' : True
            },{
                'en_itop' : [''],
                'es_itop' : ['Analista->Nombre común'],
                'ivanti'  : 'zUsuarioFallaR',
                'require_catalog' : False
            },]
    },
    'change' : {
        'client_id' : "D82B5035AFEA40A883E455FBB61D0227",
        'LoginId' : "usuario.asf",
        'OwnerTeam' : 'Mesa de servicio de Centro de Datos',
        'RequestedBy' : 'asf@test.com',
        'RequestorEmail' : 'seguerra@asf.gob.mx',
        'Sponsor' : 'Alejandro Ayala Arcipr',
        'TypeOfChange' : 'Importante',
        'OwnerTeam' : 'Mesa de servicio de Centro de Datos',
        'fields'  :  [{
                'en_itop' : [''],
                'es_itop' : ['Id (Clave Primaria)'],
                'ivanti'  : 'RecId',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Asunto'],
                'ivanti'  : 'Subject',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Descripción'],
                'ivanti'  : 'Description',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Fecha de Fin'],
                'ivanti'  : 'ScheduledEndDate',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Fecha de Inicio'],
                'ivanti'  : 'ScheduledStartDate',
                'require_catalog' : False
            },{
                'en_itop' : [''],
                'es_itop' : ['Estatus'],
                'ivanti'  : 'Status',
                'require_catalog' : True
            }]
    } 

}

def save_document(document: pd.DataFrame , _filename: str):
    global output_route
    if output_route.endswith('/') or output_route.endswith('\\'):
        output_route = output_route[:-1]
    document.to_csv("{}/{}.csv".format(output_route,_filename),index=False, encoding='latin-1')
    print('documento {} guardado en {}'.format( _filename, output_route))

def generate_catalogs_document(data: pd.DataFrame, type: str):
    global config_data
    fields = config_data[type]['fields']
    series = []

    for field in fields:
        if field['require_catalog']:
            if (field['ivanti'] in data.columns):
                series.append(pd.Series(data[field['ivanti']].drop_duplicates().reset_index(drop=True), name=field['ivanti']))

    filtered_document_df = pd.concat(series, axis=1)
    save_document(filtered_document_df, '{}_catalog'.format(type))

def create_incident_import_file(incident_df: pd.DataFrame):
    global filename
    global config_data
    fields = config_data['incident']['fields']
    export_document_df = pd.DataFrame()

    for field in fields:
        if field['es_itop'][0] in incident_df.columns:
            export_document_df[field['ivanti']] = incident_df[field['es_itop'][0]]
            export_document_df['OrgUnitLink'] = config_data['incident']['client_id']
            export_document_df['OrgUnitLink_RecID'] = config_data['incident']['client_id']
            export_document_df['ProfileLink_RecID'] = config_data['incident']['prfile_id']
            export_document_df['LoginId'] = config_data['incident']['LoginId']
            export_document_df['OwningOrgUnitId'] = config_data['incident']['OwningOrgUnitId']
            export_document_df['Owner'] = config_data['incident']['Owner']
            export_document_df['Category'] = config_data['incident']['Category']
            export_document_df['OrganizationUnitID'] = config_data['incident']['OrganizationUnitID']
            export_document_df['Email'] = config_data['incident']['Email']
            export_document_df['ProfileFullName'] = config_data['incident']['ProfileFullName']

        elif field['en_itop'][0] in incident_df.columns:
            export_document_df[field['ivanti']] = incident_df[field['en_itop'][0]]
            export_document_df['OrgUnitLink'] = config_data['incident']['client_id']
            export_document_df['OrgUnitLink_RecID'] = config_data['incident']['client_id']
            export_document_df['ProfileLink_RecID'] = config_data['incident']['prfile_id']
            export_document_df['LoginId'] = config_data['incident']['LoginId']
            export_document_df['OwningOrgUnitId'] = config_data['incident']['OwningOrgUnitId']
            export_document_df['Owner'] = config_data['incident']['Owner']
            export_document_df['Category'] = config_data['incident']['Category']
            export_document_df['OrganizationUnitID'] = config_data['incident']['OrganizationUnitID']
            export_document_df['Email'] = config_data['incident']['Email']
            export_document_df['ProfileFullName'] = config_data['incident']['ProfileFullName']


        
    if(filename == ''):
        filename = 'incident_import' 
    
    generate_catalogs_document(export_document_df, 'incident')
    save_document(export_document_df, filename)

def create_request_import_file(service_request_df: pd.DataFrame):
    global filename
    global config_data
    fields = config_data['servicerequest']['fields']
    export_document_df = pd.DataFrame()

    for field in fields:
        if field['es_itop'][0] in service_request_df.columns:
            export_document_df[field['ivanti']] = service_request_df[field['es_itop'][0]]
            export_document_df['OrgUnitLink'] = config_data['servicerequest']['client_id']
            export_document_df['LoginId'] = config_data['servicerequest']['LoginId']
            export_document_df['Service'] = config_data['servicerequest']['Service']
            export_document_df['Owner'] = config_data['servicerequest']['Owner']
            export_document_df['OrganizationUnitID'] = config_data['servicerequest']['OrganizationUnitID']
            export_document_df['Email'] = config_data['servicerequest']['Email']
            export_document_df['ProfileFullName'] = config_data['servicerequest']['ProfileFullName']

        
        elif field['en_itop'][0] in service_request_df.columns:
            export_document_df[field['ivanti']] = service_request_df[field['en_itop'][0]]
            export_document_df['OrgUnitLink'] = config_data['servicerequest']['client_id']
            export_document_df['LoginId'] = config_data['servicerequest']['LoginId']
            export_document_df['Service'] = config_data['servicerequest']['Service']
            export_document_df['Owner'] = config_data['servicerequest']['Owner']
            export_document_df['OrganizationUnitID'] = config_data['servicerequest']['OrganizationUnitID']
            export_document_df['Email'] = config_data['servicerequest']['Email']
            export_document_df['ProfileFullName'] = config_data['servicerequest']['ProfileFullName']


    if(filename == ''):
        filename = 'servicerequest_import' 
    
    generate_catalogs_document(export_document_df, 'servicerequest')
    save_document(export_document_df, filename)

def create_change_request_import_file(change_request_df: pd.DataFrame):
    global filename
    global config_data
    fields = config_data['change']['fields']
    export_document_df = pd.DataFrame()

    for field in fields:
        if field['es_itop'][0] in change_request_df.columns:
            export_document_df[field['ivanti']] = change_request_df[field['es_itop'][0]]
            export_document_df['LoginId'] = config_data['change']['LoginId']
            export_document_df['OwnerTeam'] = config_data['change']['OwnerTeam']
            export_document_df['RequestedBy'] = config_data['change']['RequestedBy']
            export_document_df['RequestorEmail'] = config_data['change']['RequestorEmail']
            export_document_df['Sponsor'] = config_data['change']['Sponsor']
            export_document_df['TypeOfChange'] = config_data['change']['TypeOfChange']
            export_document_df['OwnerTeam'] = config_data['change']['OwnerTeam']

        elif field['en_itop'][0] in change_request_df.columns:
            export_document_df[field['ivanti']] = change_request_df[field['en_itop'][0]]
            export_document_df['LoginId'] = config_data['change']['LoginId']
            export_document_df['OwnerTeam'] = config_data['change']['OwnerTeam']
            export_document_df['RequestedBy'] = config_data['change']['RequestedBy']
            export_document_df['RequestorEmail'] = config_data['change']['RequestorEmail']
            export_document_df['Sponsor'] = config_data['change']['Sponsor']
            export_document_df['TypeOfChange'] = config_data['change']['TypeOfChange']
            export_document_df['OwnerTeam'] = config_data['change']['OwnerTeam']
    if(filename == ''):
        filename = 'change_import'
    
    generate_catalogs_document(export_document_df, 'change')
    save_document(export_document_df, filename)

def process_input(args):
    global output_route
    global filename
    global config_data
    if (args.configfile):
        print('not implemented yet')
    if (args.filename):
        filename = args.filename
    if (args.output):
        output_route = args.output
    if (args.servicerequest): 
        if not args.servicerequest.lower().endswith('.csv'):
            print("Error: El archivo de service request debe ser un archivo CSV.")
            sys.exit(1)
        try:
            service_request_df = pd.read_csv(args.servicerequest, index_col=False, encoding='latin-1', low_memory=False)
            create_request_import_file(service_request_df)
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            sys.exit(1)
    if (args.incident):
        if not args.incident.lower().endswith('.csv'):
            print("Error: El archivo de incident debe ser un archivo CSV.")
            sys.exit(1)
        try:
            incident_df = pd.read_csv(args.incident, index_col=False, encoding='latin-1', low_memory=False)
            create_incident_import_file(incident_df)
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            sys.exit(1)
    if (args.change):
        if not args.change.lower().endswith('.csv'):
            print("Error: El archivo de change request debe ser un archivo CSV.")
            sys.exit(1)
        try:
            change_request_df = pd.read_csv(args.change, index_col=False, encoding='latin-1', low_memory=False)
            create_change_request_import_file(change_request_df)
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            sys.exit(1)
    if (args.showConfigFile):
        print(json.dumps(config_data, indent=4, ensure_ascii=False))

def main():

    parser = argparse.ArgumentParser(description="Script para transformar una exportacion de itop a una importacion de ivanti")
    parser.add_argument("-cf","--configfile", help="Archivo de configuracion .json",required=False)
    parser.add_argument("-os","--servicerequest", help="Archivo de itop para service request",required=False)
    parser.add_argument("-i","--incident", help="Archivo de itop para incident",required=False)
    parser.add_argument("-c","--change", help="Archivo de itop para change",required=False)
    parser.add_argument("-n","--filename", help="Nombre del archivo",required=False)
    parser.add_argument("-o","--output",help="Salida de los archivos",required=False)
    parser.add_argument("-f","--showConfigFile", action="store_true", help="Valores del archivo de configuración actual",required=False)

    args = parser.parse_args()

    if not (
        args.configfile or 
        args.servicerequest or
        args.incident or
        args.change or
        args.output or
        args.showConfigFile or
        args.filename
    ):
        print("Debe proporcionar al menos un parametro")
        parser.print_help()
        sys.exit(1)
    else: 
        process_input(args)



if __name__ == "__main__":
    main()
