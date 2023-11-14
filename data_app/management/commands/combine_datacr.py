import csv
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Combine and add status column (uppercase) to DataCR CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        input_files = ['DataCR_Approved.csv', 'DataCR_Pending.csv', 'DataCR_Rejected.csv']
        output_file = 'DataCR.csv'

        with open(os.path.join(directory_path, output_file), 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            for input_file in input_files:
                with open(os.path.join(directory_path, input_file), 'r') as infile:
                    reader = csv.reader(infile)

                    # write data
                    for row in reader:
                        # get status from file name (APPROVED, PENDING, REJECTED) and convert to uppercase
                        status = os.path.basename(input_file).split('_')[1].upper()
                        row.append(status)
                        writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"Combined data saved to {output_file}"))
