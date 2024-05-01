# This code is adapted from: https://stackoverflow.com/questions/49610125/whats-the-easiest-way-to-import-a-csv-file
# -into-a-django-model
import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Replace the contents of the PubType column in a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str, help='Path to the input CSV file')
        parser.add_argument('output_file', type=str, help='Path to the output CSV file')

    def map_pub_type(self, pub_type):
        pub_type_mapping = {
            "Book": 1,
            "Book Chapter": 2,
            "Conference Proceedings": 3,
            "Journal": 4,
            "Magazine Article": 5,
            "Report": 6,
            "Thesis": 7,
            "Unknown": 8,
            "Review Article": 9,
            "Abstract": 10,
            "Unpublished": 18,
            "Pers Comm": 19
        }
        return pub_type_mapping.get(pub_type, 8)

    def handle(self, *args, **kwargs):
        input_file = kwargs['input_file']
        output_file = kwargs['output_file']

        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            header = next(reader)

            # Find the index of the 'PubType' column and the 'PubTitleName' column
            pub_type_index = header.index('PubType')
            pub_title_name_index = header.index('PubTitleName')

            writer = csv.writer(outfile)
            writer.writerow(header)  # Write the header to the output file

            for row in reader:
                # Replace the contents of the 'PubType' column
                row[pub_type_index] = str(self.map_pub_type(row[pub_type_index]))

                writer.writerow(row)

        self.stdout.write(self.style.SUCCESS("PubType replacement completed successfully"))
