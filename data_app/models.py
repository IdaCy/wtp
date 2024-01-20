from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SALUTATION_CHOICES = [
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Miss', 'Miss'),
    ('Dr', 'Dr'),
    ('Professor', 'Professor'),
    ('Ms', 'Ms'),
    ('Other', 'Other'),
    ]

    salutation = models.CharField(max_length=20, choices=SALUTATION_CHOICES, blank=True, null=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    jobtitle = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    admin_priv = models.SmallIntegerField(default=0, null=True)


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

    def __str__(self):
        return self.pub_type_name

class PubTitle(models.Model):
    pub_title_id = models.IntegerField(primary_key=True)
    pub_title_name = models.CharField(max_length=200)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_type = models.ForeignKey(PubType, on_delete=models.CASCADE)

    def __str__(self):
        return self.pub_title_name

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
    dry_to_wet_ratio = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    ash_to_wet_ratio = models.DecimalField(max_digits=3, decimal_places=2, null=True)
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
    liver_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bone_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    muscle_to_body_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.language

class Reference(models.Model):
    ref_id = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=500)
    article_title = models.CharField(max_length=500, null=True)
    pub_title = models.ForeignKey(PubTitle, on_delete=models.CASCADE, null=True)
    year = models.CharField(max_length=30, default='', blank=True)
    volume = models.CharField(max_length=50, default='', blank=True)
    part = models.CharField(max_length=50, default='', blank=True)
    pages = models.CharField(max_length=50, default='', blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    pub_type = models.ForeignKey(PubType, on_delete=models.CASCADE, null=True)
    translation = models.CharField(max_length=5, default='', blank=True)
    keyword_1 = models.CharField(max_length=50, default='', blank=True)
    keyword_2 = models.CharField(max_length=50, default='', blank=True)
    keyword_3 = models.CharField(max_length=50, default='', blank=True)
    keyword_4 = models.CharField(max_length=50, default='', blank=True)
    notes = models.CharField(max_length=500, default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dc_id = models.IntegerField()
    approval_status = models.CharField(max_length=20)
    reason_approval_delete = models.CharField(max_length=500, default='', blank=True)


class DataCR(models.Model):
    cr_id = models.IntegerField(primary_key=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE, null=True)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE, null=True)
    icrp_rap = models.ForeignKey(RAP, on_delete=models.CASCADE, null=True)
    lifestage = models.ForeignKey(Lifestage, on_delete=models.CASCADE, null=True)
    species_name = models.ForeignKey(SpeciesName, on_delete=models.CASCADE, null=True)
    study_type = models.ForeignKey(StudyType, on_delete=models.CASCADE, null=True)
    measurement_date = models.CharField(max_length=50, null=True)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE, null=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True)
    crn = models.IntegerField(null=True) # or? models.SmallIntegerField(null=True)
    cr = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    cr_sd = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    notes = models.CharField(max_length=500, null=True)
    radionuclide = models.ForeignKey(Radionuclide, on_delete=models.CASCADE, null=True)
    from_erica = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    biohalflife = models.CharField(max_length=30, null=True)
    biota_conc = models.CharField(max_length=30, null=True)
    biota_conc_unit_choices = [
        ('µCi/kg', 'µCi/kg'),
        ('Bq/kg', 'Bq/kg'),
        ('Bg/kg fresh', 'Bg/kg fresh'),
        ('Bg/kg FW', 'Bg/kg FW'),
        ('Bq/l', 'Bq/l'),
        ('mg/kg fresh', 'mg/kg fresh'),
        ('mg/kg', 'mg/kg'),
        ('mg/kg FW', 'mg/kg FW'),
        ('Bq/m3', 'Bq/m3'),
    ]
    biota_conc_units = models.CharField(max_length=20, choices=biota_conc_unit_choices, default='Bq/kg', null=True, blank=True )
    biota_n = models.IntegerField(null=True)
    biota_sd = models.CharField(max_length=30, null=True)
    biota_wet_dry_choices = [
        ('W', 'Wet'),
        ('D', 'Dry'),
        ('A', 'Air'),
    ]
    biota_wet_dry = models.CharField(max_length=20, choices=biota_wet_dry_choices, default='W', null=True, blank=True )
    data_extract = models.IntegerField(null=True)
    media_conc = models.CharField(max_length=30, null=True)
    media_n = models.CharField(max_length=30, null=True)
    media_conc_unit_choices = [
        ('Bq/kg', 'Bq/kg'),
        ('Bq/l', 'Bq/l'),
        ('Bq/m3', 'Bq/m3'),
        ('mBq/l', 'mBq/l'),
        ('mg/kg', 'mg/kg'),
    ]
    media_conc_units = models.CharField(max_length=20, choices=media_conc_unit_choices, default='Bq/kg', null=True, blank=True )
    media_sd = models.CharField(max_length=30, null=True)
    media_wet_dry_choices = [
        ('W', 'Wet'),
        ('D', 'Dry'),
        ('A', 'Air'),
    ]
    media_wet_dry = models.CharField(max_length=5, choices=media_wet_dry_choices, default='W', null=True, blank=True )
    other_tissue = models.CharField(max_length=30, null=True)
    qc = models.BooleanField(default=False)
    rep_organ_units = models.CharField(max_length=30, null=True)
    reproductive_organ = models.CharField(max_length=30, null=True)
    rep_wet_dry_choices = [
        ('W', 'Wet'),
        ('D', 'Dry'),
        ('A', 'Air'),
    ]
    rep_wet_dry = models.CharField(max_length=5, choices=rep_wet_dry_choices, default='W', null=True, blank=True )
    stand_biota_conc = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    stand_biota_sd = models.CharField(max_length=30, null=True)
    stand_media_conc = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    stand_media_sd = models.CharField(max_length=30, null=True)
    summary_approve = models.BooleanField(default=False)
    approval_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    approval_data_status = models.CharField(max_length=20, choices=approval_choices, default='PENDING')
