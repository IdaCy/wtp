from django.core.management.base import BaseCommand
from data_app.models import ParCRCalc

class Command(BaseCommand):
    help = 'Custom command for data_app customization'

    def handle(self, *args, **kwargs):
        # Delete all rows in the table
        ParCRCalc.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully emptied the ParCRCalc table'))
