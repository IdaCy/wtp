from django.db import models
from django.contrib.auth.models import User


class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)
    element_symbol = models.CharField(max_length=10)
    approved = models.BooleanField(default=False)


class Habitat(models.Model):
    habitat_id = models.IntegerField(primary_key=True)
    habitat_specific_type = models.CharField(max_length=200)
    habitat_main_type_id = models.SmallIntegerField()
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WildlifeGroup(models.Model):
    wildlife_group_id = models.IntegerField(primary_key=True)
    wildlife_group_name = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    data_extract = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    de_tophab_topwild = models.IntegerField()
    de_tophab_indwild = models.IntegerField()
    de_indhab_topwild = models.IntegerField()
    de_indhab_indwild = models.IntegerField()


class RAP(models.Model):
    rap_id = models.IntegerField(primary_key=True)
    rap_name = models.CharField(max_length=200)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE)
    summary = models.CharField(max_length=200)


class Lifestage(models.Model):
    lifestage_id = models.IntegerField(primary_key=True)
    lifestage_name = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    rap = models.ForeignKey(RAP, on_delete=models.CASCADE)


class Media(models.Model):
    media_id = models.IntegerField(primary_key=True)
    media_type = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)


class PubType(models.Model):
    pub_type_id = models.IntegerField(primary_key=True)
    pub_type_name = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PubTitle(models.Model):
    pub_title_id = models.IntegerField(primary_key=True)
    pub_title_name = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_type = models.ForeignKey(PubType, on_delete=models.CASCADE)


class SpeciesName(models.Model):
    species_id = models.IntegerField(primary_key=True)
    name_latin = models.CharField(max_length=200)
    name_common = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StudyType(models.Model):
    study_type_id = models.IntegerField(primary_key=True)
    study_type_name = models.CharField(max_length=50)


class Tissue(models.Model):
    tissue_id = models.IntegerField(primary_key=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correction_factor_tissue = models.DecimalField(max_digits=10, decimal_places=3)


class MaterialStatus(models.Model):
    material_status_id = models.IntegerField(primary_key=True)
    material_status_name = models.CharField(max_length=50)
    correction_ratio = models.DecimalField(max_digits=10, decimal_places=3)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)


class ActivityConcUnit(models.Model):
    act_conc_unit_id = models.AutoField(primary_key=True)
    act_conc_unit_symbol = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    correction_factor_act_conc = models.DecimalField(max_digits=10, decimal_places=3)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)


class ParCRCalc(models.Model):
    cr_id = models.IntegerField(primary_key=True)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    dry_to_wet_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    ash_to_wet_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    fmt_choices = [
        ('F', 'Freshwater'),
        ('M', 'Marine'),
        ('T', 'Terrestrial'),
    ]
    is_fre_mar_ter = models.CharField(max_length=1, choices=fmt_choices)


class MaterialCRCalc(models.Model):
    cr_id = models.IntegerField(primary_key=True)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    organism = models.IntegerField()
    liver_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    bone_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    muscle_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    fmt_choices = [
        ('F', 'Freshwater'),
        ('M', 'Marine'),
        ('T', 'Terrestrial'),
    ]
    is_fre_mar_ter = models.CharField(max_length=1, choices=fmt_choices)


class Radionuclide(models.Model):
    radionuclide_id = models.IntegerField(primary_key=True)
    radionuclide_name = models.CharField(max_length=50)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    user_id = models.IntegerField()


class Reference(models.Model):
    ref_id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=500)
    article_title = models.CharField(max_length=500)
    pub_title = models.ForeignKey(PubTitle, on_delete=models.CASCADE)
    year = models.SmallIntegerField()
    volume = models.SmallIntegerField()
    part = models.CharField(max_length=20)
    pages = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    pub_type = models.ForeignKey(PubType, on_delete=models.CASCADE)
    translation = models.CharField(max_length=5)
    keyword_1 = models.CharField(max_length=50)
    keyword_2 = models.CharField(max_length=50)
    keyword_3 = models.CharField(max_length=50)
    keyword_4 = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dc_id = models.IntegerField()
    approval_status = models.CharField(max_length=20)
    reason_approval_delete = models.CharField(max_length=500)


class DataCR(models.Model):
    cr_id = models.IntegerField(primary_key=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE)
    icrp_rap = models.ForeignKey(RAP, on_delete=models.CASCADE)
    lifestage = models.ForeignKey(Lifestage, on_delete=models.CASCADE)
    species_name = models.ForeignKey(SpeciesName, on_delete=models.CASCADE)
    study_type = models.ForeignKey(StudyType, on_delete=models.CASCADE)
    measurement_date = models.DateField()
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    crn = models.SmallIntegerField()
    cr = models.IntegerField()
    cr_sd = models.IntegerField()
    notes = models.CharField(max_length=500)
    radionuclide = models.ForeignKey(Radionuclide, on_delete=models.CASCADE)
    from_erica = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    biohalflife = models.CharField(max_length=30)
    biota_conc = models.DecimalField(max_digits=25, decimal_places=15)
    biota_conc_unit_choices = [
        ('µCi/kg', 'µCi/kg'),
        ('Bq/kg', 'Bq/kg'),
        ('Bg/kg fresh', 'Bg/kg fresh'),
        ('Bg/kg FW', 'Bg/kg FW'),
        ('Bq/l', 'Bq/l'),
        ('mg/kg fresh', 'mg/kg fresh'),
        ('bg/kg FW', 'bg/kg FW'),
    ]
    biota_conc_units = models.CharField(max_length=20, choices=biota_conc_unit_choices, default='Bq/kg', )
    biota_n = models.IntegerField()
    biota_sd = models.CharField(max_length=30)
    biota_wet_dry = models.CharField(max_length=30)
    data_extract = models.IntegerField()
    media_conc = models.DecimalField(max_digits=10, decimal_places=3)
    media_n = models.CharField(max_length=30)
    media_conc_unit_choices = [
        ('Bq/kg', 'Bq/kg'),
        ('Bq/l', 'Bq/l'),
        ('mBq/l', 'mBq/l'),
    ]
    media_conc_units = models.CharField(max_length=20, choices=media_conc_unit_choices, default='Bq/kg', )
    media_sd = models.CharField(max_length=30)
    media_wet_dry_choices = [
        ('W', 'Wet'),
        ('D', 'Dry'),
    ]
    media_wet_dry = models.CharField(max_length=1, choices=media_wet_dry_choices, default='W', )
    other_tissue = models.BooleanField(default=False)
    qc = models.CharField(max_length=30)
    rep_organ_units = models.CharField(max_length=30)
    reproductive_organ = models.CharField(max_length=30)
    rep_wet_dry_choices = [
        ('W', 'Wet'),
        ('D', 'Dry'),
    ]
    rep_wet_dry = models.CharField(max_length=1, choices=rep_wet_dry_choices, default='W')
    stand_biota_conc = models.DecimalField(max_digits=10, decimal_places=3)
    stand_biota_sd = models.CharField(max_length=30)
    stand_media_conc = models.DecimalField(max_digits=10, decimal_places=3)
    stand_media_sd = models.CharField(max_length=30)
    summary_approve = models.BooleanField(default=False)
    approval_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    approval_data_status = models.CharField(max_length=20, choices=approval_choices, default='PENDING')
