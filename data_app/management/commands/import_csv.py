import os
import csv
from django.core.management.base import BaseCommand
from data_app.models import (
    Client, EditTable, Element, Habitat, Language, Lifestage, Location, Media, PubTitle, PubType,
    SpeciesName, StudyType, Tissue, MaterialStatus, Wildlife, ActivityConcentrationUnit, ParCRCalc,
    MaterialCRCalc, Radionuclide, RAP, Reference, DataCR
)


class Command(BaseCommand):
    help = 'Import data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

        for csv_file in csv_files:
            csv_file_path = os.path.join(directory_path, csv_file)
            self.import_data(csv_file_path)

    def import_data(self, csv_file):
        model_mapping = {
            'Client': Client, 'EditTable': EditTable, 'Element': Element,
            'Habitat': Habitat, 'Language': Language, 'Lifestage': Lifestage,
            'Location': Location, 'Media': Media, 'PubTitle': PubTitle,
            'PubType': PubType, 'SpeciesName': SpeciesName, 'StudyType': StudyType,
            'Tissue': Tissue, 'MaterialStatus': MaterialStatus, 'Wildlife': Wildlife,
            'ActivityConcentrationUnit': ActivityConcentrationUnit, 'ParCRCalc': ParCRCalc,
            'MaterialCRCalc': MaterialCRCalc, 'Radionuclide': Radionuclide, 'RAP': RAP,
            'Reference': Reference, 'DataCR': DataCR,
        }

        model_name = os.path.splitext(os.path.basename(csv_file))[0]
        if model_name not in model_mapping:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found. Skipping..."))
            return

        model = model_mapping[model_name]

        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obj, created = model.objects.get_or_create(**row)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported {model_name} {obj}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"{model_name} {obj} already exists. Skipping..."))
