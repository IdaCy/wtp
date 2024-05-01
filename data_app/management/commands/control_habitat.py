# This code is adapted from: https://stackoverflow.com/questions/49610125/whats-the-easiest-way-to-import-a-csv-file
# -into-a-django-model
import csv
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Modify and write CSV file'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        input_file = 'Habitat.csv'
        output_file = 'Habitat-rearranged.csv'

        with open(os.path.join(directory_path, input_file), 'r') as infile:
            reader = csv.reader(infile)
            header = next(reader)

            # Find the index of the 'Approved' column
            approved_index = header.index('Approved')

            # Find the index of the 'MainHabitatType' column
            main_habitat_type_index = header.index('MainHabitatType')

            # Find the index of the 'UserID' column
            user_id_index = header.index('UserID')

            # Modify the header to rearrange columns
            header = [
                'HabitatID', 'Habitat', 'MainHabitatType', 'Approved', 'UserID'
            ]

            with open(os.path.join(directory_path, output_file), 'w', newline='') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

                # Write modified header
                writer.writerow(header)

                # Write data
                for row in reader:
                    # Rearrange the columns
                    rearranged_row = [
                        row[header.index('HabitatID')],
                        row[header.index('Habitat')],
                        row[main_habitat_type_index],
                        row[approved_index],
                        row[user_id_index]
                    ]

                    writer.writerow(rearranged_row)

        self.stdout.write(self.style.SUCCESS(f"Modified data saved to {output_file}"))
