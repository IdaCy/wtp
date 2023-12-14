import csv
from django.core.management.base import BaseCommand

from data_app.models import ParCRCalc


class Command(BaseCommand):
    help = 'Update ParCRCalc CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the ParCRCalc CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Read CSV file and update values
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # Update values in the specified columns
            for row in rows:
                try:
                    row['WildlifeGroupId'] = int(float(row['WildlifeGroupId']))
                    row['TissueId'] = int(float(row['TissueId']))
                except ValueError:
                    self.stdout.write(self.style.ERROR("Invalid value found. Skipping..."))
                    continue

            # Write updated data to a new CSV file
            output_file_path = file_path.replace('.csv', '_updated.csv')
            with open(output_file_path, 'w', newline='') as outfile:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            self.stdout.write(self.style.SUCCESS(f"Updated data saved to {output_file_path}"))