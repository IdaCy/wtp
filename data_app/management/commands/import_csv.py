from django.core.management.base import BaseCommand, CommandError
from data_app.models import (Element, Habitat, WildlifeGroup, RAP, Lifestage, Media, PubType, PubTitle,
                             SpeciesName, StudyType, Tissue, MaterialStatus, ActivityConcUnit, ParCRCalc,
                             MaterialCRCalc, Radionuclide, Language, Reference, DataRC)
import pandas as pd
import os


class Command(BaseCommand):
    help = 'Imports data from Excel files into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the directory containing Excel files')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.isdir(file_path):
            raise CommandError(f'"{file_path}" is not a valid directory')

        for model in [Element, Habitat, WildlifeGroup, ...]:
            file_name = os.path.join(file_path, model.__name__ + '.xlsx')
            if os.path.exists(file_name):
                self.stdout.write(f'Importing data for {model.__name__}...')
                data = pd.read_excel(file_name)
                model.objects.bulk_create(model(**row) for index, row in data.iterrows())
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {model.__name__}'))
            else:
                self.stdout.write(self.style.WARNING(f'No file found for {model.__name__}, skipping'))

        self.stdout.write(self.style.SUCCESS('Data import complete'))
