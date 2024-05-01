# This code is adapted from: https://stackoverflow.com/questions/70984787/cant-populate-database-by-excel-file-in
# -django-management-command
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from data_app.models import Element, Habitat, WildlifeGroup, RAP, Lifestage, Media, PubType, PubTitle, SpeciesName, StudyType, Tissue, MaterialStatus, ActivityConcUnit, ParCRCalc, MaterialCRCalc, Radionuclide, Language, Reference, ReferenceRejectionReason, DataCR

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

        for model in [Element, Habitat, WildlifeGroup, RAP, Lifestage, Media, PubType, PubTitle, SpeciesName, StudyType, Tissue, MaterialStatus, ActivityConcUnit, ParCRCalc, MaterialCRCalc, Radionuclide, Language, Reference, ReferenceRejectionReason, DataCR]:
            file_name = os.path.join(file_path, model.__name__ + '.xlsx')
            if os.path.exists(file_name):
                self.stdout.write(f'Importing data for {model.__name__}...')
                data = pd.read_excel(file_name)

                instances = []
                for index, row in data.iterrows():
                    row_data = row.to_dict()
                    for field in model._meta.fields:
                        if isinstance(field, models.ForeignKey):
                            # Handle foreign key fields
                            fk_model = field.related_model
                            fk_field_name = field.name
                            fk_id = row_data.get(fk_field_name)

                            if pd.isna(fk_id):
                                row_data[fk_field_name] = None
                            else:
                                try:
                                    fk_instance = fk_model.objects.get(pk=fk_id)
                                    row_data[fk_field_name] = fk_instance
                                except ObjectDoesNotExist:
                                    if field.null:
                                        row_data[fk_field_name] = None
                                    else:
                                        self.stdout.write(self.style.WARNING(
                                            f"Skipping row {index} in {model.__name__}: "
                                            f"Related {fk_model.__name__} with ID {fk_id} does not exist."
                                        ))
                                        continue
                        elif isinstance(field, models.BooleanField):
                            # Handle Boolean fields
                            field_name = field.name
                            field_value = row_data.get(field_name)
                            if pd.isna(field_value):
                                if field.null:
                                    row_data[field_name] = None
                                else:
                                    self.stdout.write(self.style.WARNING(
                                        f"Skipping row {index} in {model.__name__}: "
                                        f"NaN found in non-nullable Boolean field {field_name}."
                                    ))
                                    continue
                            else:
                                choices = getattr(field, 'choices', [(True, 'True'), (False, 'False')])  # Provide default choices
                                row_data[field_name] = self.convert_to_boolean(field_value, choices, field.default)

                        elif isinstance(field, (models.DecimalField, models.IntegerField)):
                            # Handle decimal and integer fields
                            field_name = field.name
                            field_value = row_data.get(field_name)
                            if pd.isna(field_value):
                                if field.null:
                                    row_data[field_name] = None
                                else:
                                    self.stdout.write(self.style.WARNING(
                                        f"Setting row {index} in {model.__name__}: "
                                        f"NaN found in non-nullable numeric field {field_name} to None."
                                    ))
                                    row_data[field_name] = None

                    instances.append(model(**row_data))

                model.objects.bulk_create(instances)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {model.__name__}'))
            else:
                self.stdout.write(self.style.WARNING(f'No file found for {model.__name__}, skipping'))

        self.stdout.write(self.style.SUCCESS('Data import complete'))

    def convert_to_boolean(self, value, choices, default):
        # If choices is None or empty, use default choices for Boolean
        if not choices:
            choices = [(True, 'True'), (False, 'False')]

        # Prepare a set of valid choices (both keys and values)
        valid_choices = set()
        for key, val in choices:
            valid_choices.add(key)
            valid_choices.add(str(val).lower())

        # Check and convert the value
        if isinstance(value, str):
            value_lower = value.lower()
            if value_lower in valid_choices:
                return value_lower == 'true'
        elif value in valid_choices:
            return bool(value)

        # If value is not in choices, set to default
        self.stdout.write(self.style.WARNING(
            f"Value '{value}' not in choices, setting to default value '{default}'."
        ))
        return default
