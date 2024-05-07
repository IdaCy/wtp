from django.contrib import admin
from .models import DataCR, PubType, PubTitle, Language, Reference, Habitat, SpeciesName, ReferenceRejectionReason, RAP, \
    Media, WildlifeGroup, Element, Radionuclide, Tissue


class DataCRAdmin(admin.ModelAdmin):
    list_display = ['cr', 'cr_n', 'media_conc', 'biota_conc', 'approval_status']
    list_filter = ('approval_status',)
    search_fields = ['cr', 'media_conc_units']
    ordering = ('-approval_status', 'cr_id')


admin.site.register(DataCR, DataCRAdmin)
admin.site.register(PubType)
admin.site.register(PubTitle)
admin.site.register(Language)
admin.site.register(Reference)
admin.site.register(Habitat)
admin.site.register(SpeciesName)
admin.site.register(ReferenceRejectionReason)
admin.site.register(Media)
admin.site.register(WildlifeGroup)
admin.site.register(Element)
admin.site.register(Radionuclide)
admin.site.register(Tissue)
