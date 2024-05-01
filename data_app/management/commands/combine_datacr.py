# This code is adapted from: https://stackoverflow.com/questions/49610125/whats-the-easiest-way-to-import-a-csv-file
# -into-a-django-model
import csv
import os
from django.core.management.base import BaseCommand


# Custom Django management command to combine CSV files and add an 'origin' column (tracking table origin to know if
# accepted/rejected/pending)
class Command(BaseCommand):
    help = 'Combine and add origin column to DataCR CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    # Handle method called when the command is executed
    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        approved_file = 'DataCR_APPROVED.csv'
        rejected_file = 'DataCR_REJECTED.csv'
        output_file = 'DataCR.csv'

        # Open the output file for writing
        with open(os.path.join(directory_path, output_file), 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)

            # Iterate through each input file and its corresponding origin
            for input_file, origin in [(approved_file, 'APPROVED'), (rejected_file, 'REJECTED')]:
                with open(os.path.join(directory_path, input_file), 'r', encoding='latin-1') as infile:
                    reader = csv.reader(infile)

                    # Write data to the output file
                    for row in reader:
                        # Add the origin column
                        row.append(origin)
                        writer.writerow(row)

        # Display a success message after processing
        self.stdout.write(self.style.SUCCESS(f"Combined data saved to {output_file}"))
