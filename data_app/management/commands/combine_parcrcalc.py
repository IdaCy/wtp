# This code is adapted from: https://stackoverflow.com/questions/49610125/whats-the-easiest-way-to-import-a-csv-file
# -into-a-django-model
import csv
import os
from django.core.management.base import BaseCommand


# Command to combine and add column to CSV files.
class Command(BaseCommand):
    help = 'Combine and add origin column to CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        input_files = ['Biota_Fres_CF.csv', 'Biota_Mar_CF.csv', 'Biota_Ter_CF.csv']
        output_file = 'ParCRCalc.csv'

        with open(os.path.join(directory_path, output_file), 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            for input_file in input_files:
                with open(os.path.join(directory_path, input_file), 'r') as infile:
                    reader = csv.reader(infile)

                    # Write data
                    for row in reader:
                        # Sixth character of each file name indicates the origin (F, M, T)
                        row.append(os.path.basename(input_file)[6])  # Extract F, M, or T from  filename
                        writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"Combined data saved to {output_file}"))
