import csv
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Combine and add origin column to MaterialCRCalc CSV files'

    def add_arguments(self, parser):
        parser.add_argument('directory_path', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['directory_path']
        input_files = ['Fresh_CF.csv', 'Mar_CF.csv', 'Terr_CF.csv']
        output_file = 'MaterialCRCalc.csv'

        with open(os.path.join(directory_path, output_file), 'w', newline='') as outfile:
            writer = csv.writer(outfile)

            for input_file in input_files:
                with open(os.path.join(directory_path, input_file), 'r') as infile:
                    reader = csv.reader(infile)

                    # write data
                    for row in reader:
                        # first character of each file name indicates the origin (F, M, T)
                        row.append(os.path.basename(input_file)[0])  # extract F, M, or T from  filename
                        writer.writerow(row)

        self.stdout.write(self.style.SUCCESS(f"Combined data saved to {output_file}"))
