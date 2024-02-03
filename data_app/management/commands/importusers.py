from django.contrib.auth import get_user_model
import pandas as pd
import os
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Imports data from Excel files into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the directory containing Excel files')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.isdir(file_path):
            raise CommandError(f'"{file_path}" is not a valid directory')

        User = get_user_model()

        file_name = os.path.join(file_path, User.__name__ + '.xlsx')
        if os.path.exists(file_name):
            self.stdout.write(f'Importing data for {User.__name__}...')
            data = pd.read_excel(file_name)

            instances = []
            for index, row in data.iterrows():
                row_data = row.to_dict()
                salutation = row_data.get('salutation')
                firstname = row_data.get('firstname')
                lastname = row_data.get('lastname')
                email = row_data.get('email')
                jobtitle = row_data.get('jobtitle')
                company = row_data.get('company')
                admin_priv = row_data.get('admin_priv')

                # Use the create_user method to create a user instance
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=None,
                )

                # Set additional fields
                user.salutation = salutation
                user.first_name = firstname
                user.last_name = lastname
                user.jobtitle = jobtitle
                user.company = company
                user.admin_priv = admin_priv

                user.save()  # Save the user instance
                instances.append(user)

            self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {User.__name__}'))
        else:
            self.stdout.write(self.style.WARNING(f'No file found for {User.__name__}, skipping'))

        self.stdout.write(self.style.SUCCESS('Data import complete'))
