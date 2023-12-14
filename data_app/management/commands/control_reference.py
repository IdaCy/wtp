import csv
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Convert space-separated CSV to comma-separated with semicolon'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str, help='Path to the input CSV file')
        parser.add_argument('output_file', type=str, help='Path to the output CSV file')

    def handle(self, *args, **kwargs):
        input_file = kwargs['input_file']
        output_file = kwargs['output_file']

        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        # Replace spaces with commas
        modified_lines = [line.replace(' ', ',') for line in lines]

        with open(output_file, 'w') as outfile:
            outfile.writelines(modified_lines)

        self.stdout.write(self.style.SUCCESS(f"Conversion completed. Output saved to {output_file}"))
