import csv
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Combine and add origin column to DataCR CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        approved_file = 'DataCR_APPROVED.csv'
        rejected_file = 'DataCR_REJECTED.csv'
        output_file = 'DataCR.csv'

        with open(os.path.join(directory_path, output_file), 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)

            for input_file, origin in [(approved_file, 'APPROVED'), (rejected_file, 'REJECTED')]:
                with open(os.path.join(directory_path, input_file), 'r', encoding='latin-1') as infile:
                    reader = csv.reader(infile)

                    # write data
                    for row in reader:
                        # add the origin column
                        row.append(origin)
                        writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"Combined data saved to {output_file}"))
