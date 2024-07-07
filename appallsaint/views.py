from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def menu_view(request):
    # Configura el alcance de la API y las credenciales
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('appallsaint/credentials/credentials.json', scope)
    client = gspread.authorize(credentials)

    # Abre la hoja de cálculo deseada usando la clave de la hoja (sheet key)
    sheet = client.open_by_key('1SDNLkmf_lIPtR777XG_MjLTcJjY8EqaU8IV2hnMju3k').sheet1  # Reemplaza 'TU_SHEET_KEY' con la clave de tu hoja de cálculo

    # Obtén todos los registros de la hoja
    records = sheet.get_all_records()

    # Procesa los datos de Google Sheets como items del menú
    categories = {}
    for record in records:
        category = record['Categoria']  # Asegúrate de que los nombres de las columnas coincidan con los de tu hoja
        item = {
            'name': record['Nombre'],
            'description': record['Descripción'],
            'price': record['Precio'],
        }
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    return render(request, 'menu.html', {'categories': categories})