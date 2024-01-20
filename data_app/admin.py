from django.contrib import admin

from .models import DataCR, Reference, ParCRCalc, WildlifeGroup

admin.site.register(DataCR)
admin.site.register(Reference)
admin.site.register(ParCRCalc)
admin.site.register(WildlifeGroup)
