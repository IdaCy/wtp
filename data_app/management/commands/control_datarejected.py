# This code is adapted from: https://stackoverflow.com/questions/49610125/whats-the-easiest-way-to-import-a-csv-file
# -into-a-django-model
import csv
import os

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Modify and write CSV file'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        input_file = 'DataCR_REJ.csv'
        output_file = 'DataCR_REJECTED.csv'

        with open(os.path.join(directory_path, input_file), 'r') as infile:
            reader = csv.reader(infile)
            header = next(reader)

            # Find the index of the 'BiotaWetdry' column
            biota_wetdry_index = header.index('BiotaWetdry')

            # Find the index of the 'dataextract' column
            dataextract_index = header.index('dataextract')

            # Modify the header to place 'dataextract' after 'BiotaWetdry'
            header.insert(biota_wetdry_index + 1, header.pop(dataextract_index))

            with open(os.path.join(directory_path, output_file), 'w', newline='') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

                # Write modified header
                writer.writerow(header)

                # Write data
                for row in reader:
                    # Move 'biohalflife'/'dataextract' value to the new position
                    row.insert(biota_wetdry_index + 1, row.pop(dataextract_index))
                    writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"Modified data saved to {output_file}"))
