import os
from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def menu_view(request):
    # Configura el alcance de la API y las credenciales
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Leer la ruta del archivo de credenciales desde la variable de entorno
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    print('Credentials path:', credentials_path)  # Imprime la ruta de las credenciales

    # Cargar las credenciales desde el archivo JSON
    with open(credentials_path, 'r') as f:
        credentials_dict = json.load(f)
    
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