from django.core.management.base import BaseCommand
import pandas as pd
from webpage.models import Data


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # data = pd.read_excel(r'database_yasuj.xlsx', engine='openpyxl', sheet_name='Sheet1')
        data = pd.read_excel(r'database_esfahan.xlsx', engine='openpyxl', sheet_name='Sheet1')

        for i in data.iterrows():
            # print('location', i[1]['location'])
            # print('temp', i[1]['temperature'])
            # print('time', i[1]['time'])
            # print('date', i[1]['date'])
            created = Data.objects.get_or_create(location=i[1]['location'], temperature=i[1]['temperature'],time=i[1]['time'],date=i[1]['date'])
            # City.objects.get_or_create(province=pr_of_inv, name=i[1]['City'])
            # Data.objects.all().delete()