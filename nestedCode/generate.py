import pandas as pd
import modules.headers as hdrs
import modules.convert as cvrt

try:
    conf_df = pd.read_csv('./files/config.csv', index_col=False, encoding='latin-1', low_memory=False) 
except FileNotFoundError:
    print("No se encontro el archivo ./files/config.csv")

    


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

