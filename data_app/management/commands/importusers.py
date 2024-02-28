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

            #instances = []
            for index, row in data.iterrows():
                email = row['email']
                password = row['password']  # Assuming there's a 'password' column in the Excel file

                user, created = User.objects.get_or_create(
                    username=email,
                    email=email,
                    defaults={
                        'first_name': row.get('firstname', ''),
                        'last_name': row.get('lastname', ''),
                        'jobtitle': row.get('jobtitle', ''),
                        'company': row.get('company', ''),
                        'admin_priv': row.get('admin_priv', 0),
                        'salutation': row.get('salutation', ''),
                    }
                )

                if created:
                    user.set_password(password)
                    user.save()
                #instances.append(user)

            self.stdout.write(self.style.SUCCESS(f'Successfully imported data for {User.__name__}'))
        else:
            self.stdout.write(self.style.WARNING(f'No file found for {User.__name__}, skipping'))

        self.stdout.write(self.style.SUCCESS('Data import complete'))
