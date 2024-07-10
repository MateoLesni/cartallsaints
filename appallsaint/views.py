import os
from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def menu_view(request):
    # Configura el alcance de la API y las credenciales
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Obtener las variables de entorno
    service_account_type = os.getenv('SERVICE_ACCOUNT_TYPE')
    project_id = os.getenv('PROJECT_ID')
    private_key_id = os.getenv('private_key_id')
    private_key = os.getenv('private_key').replace('\\n', '\n')
    client_email = os.getenv('client_email')
    client_id = os.getenv('client_id')
    auth_uri = os.getenv('auth_uri')
    token_uri = os.getenv('token_uri')
    auth_provider_x509_cert_url = os.getenv('auth_provider_x509_cert_url')
    client_x509_cert_url = os.getenv('client_x509_cert_url')

    # Construir las credenciales como un diccionario
    credentials_dict = {
        "type": service_account_type,
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": auth_uri,
        "token_uri": token_uri,
        "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
        "client_x509_cert_url": client_x509_cert_url
    }

    # Crear las credenciales usando el diccionario
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(credentials)

    # Abre la hoja de cálculo deseada usando la clave de la hoja (sheet key)
    sheet = client.open_by_key('1SDNLkmf_lIPtR777XG_MjLTcJjY8EqaU8IV2hnMju3k').sheet1

    # Obtén todos los registros de la hoja
    records = sheet.get_all_records()

    # Procesa los datos de Google Sheets como items del menú
    categories = {}
    for record in records:
        category = record['Categoria']
        item = {
            'name': record['Nombre'],
            'description': record['Descripción'],
            'price': record['Precio'],
        }
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    return render(request, 'menu.html', {'categories': categories})