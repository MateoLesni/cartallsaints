import pandas as pd
from django.core.management.base import BaseCommand
from appallsaint.models import MenuItem

class Command(BaseCommand):
    help = 'Carga los datos desde un archivo Excel a la base de datos'

    def handle(self, *args, **options):
        # Limpiar la base de datos antes de cargar los datos
        MenuItem.objects.all().delete()

        df = pd.read_excel(r'C:\Users\gesti\OneDrive\Desktop\bdexcel.xlsx')
        # Iterar sobre las filas del DataFrame y guardar los datos en la base de datos
        for index, row in df.iterrows():
            # Verificar si el artículo ya existe en la base de datos
            if not MenuItem.objects.filter(name=row['Nombre']).exists():
                # Si el artículo no existe, crear uno nuevo
                MenuItem.objects.create(
                    name=row['Nombre'],
                    description=row['Descripción'],
                    price=row['Precio'],
                    categories=row['Categoria']
                )

        self.stdout.write(self.style.SUCCESS('¡Datos cargados exitosamente!'))