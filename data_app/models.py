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
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    jobtitle = models.CharField(max_length=200, blank=True, null=True)
    organisation = models.CharField(max_length=200, blank=True, null=True)
    admin_priv = models.SmallIntegerField(default=0, null=True)

    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        # Handle the case where first_name or last_name might be None
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else self.email


class Element(models.Model):
    element_id = models.IntegerField(primary_key=True)
    element_symbol = models.CharField(max_length=10)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.element_symbol


class Habitat(models.Model):
    habitat_id = models.IntegerField(primary_key=True)
    habitat_specific_type = models.CharField(max_length=200)
    habitat_main_type_id = models.SmallIntegerField()
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.habitat_specific_type


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

    def __str__(self):
        return self.wildlife_group_name


class RAP(models.Model):
    rap_id = models.IntegerField(primary_key=True)
    rap_name = models.CharField(max_length=200)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE)
    summary = models.CharField(max_length=200)

    def __str__(self):
        return self.rap_name


class Lifestage(models.Model):
    lifestage_id = models.IntegerField(primary_key=True)
    lifestage_name = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    rap = models.ForeignKey(RAP, on_delete=models.CASCADE)

    def __str__(self):
        return self.lifestage_name


class Media(models.Model):
    media_id = models.IntegerField(primary_key=True)
    media_type = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.media_id} ({self.media_type})"

    def get_media_id(self):
        return str(self.media_id)

    def get_media_type(self):
        return str(self.media_type)


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

    def __str__(self):
        return f"{self.name_latin} ({self.name_common})"

    def get_name_latin(self):
        return str(self.name_latin)

    def get_name_common(self):
        return str(self.name_common)


class StudyType(models.Model):
    study_type_id = models.IntegerField(primary_key=True)
    study_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.study_type_name


class Tissue(models.Model):
    tissue_id = models.IntegerField(primary_key=True)
    tissue_name = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correction_factor_tissue = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.tissue_name


class MaterialStatus(models.Model):
    material_status_id = models.IntegerField(primary_key=True)
    material_status_name = models.CharField(max_length=50)
    correction_ratio = models.DecimalField(max_digits=10, decimal_places=3)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return self.material_status_name


class ActivityConcUnit(models.Model):
    act_conc_unit_id = models.AutoField(primary_key=True)
    act_conc_unit_symbol = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    correction_factor_act_conc = models.DecimalField(max_digits=10, decimal_places=3)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return self.correction_factor_act_conc


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

    def __str__(self):
        return f"{str(self.dry_to_wet_ratio)} ({str(self.ash_to_wet_ratio)})"

    def get_dry_to_wet_ratio(self):
        return self.dry_to_wet_ratio

    def get_ash_to_wet_ratio(self):
        return self.ash_to_wet_ratio


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

    def __str__(self):
        return f"{str(self.liver_to_body_ratio)} ({str(self.bone_to_body_ratio)}) ({str(self.muscle_to_body_ratio)})"

    def get_liver_to_body_ratio(self):
        return self.liver_to_body_ratio

    def get_bone_to_body_ratio(self):
        return self.bone_to_body_ratio

    def get_muscle_to_body_ratio(self):
        return self.muscle_to_body_ratio


class Radionuclide(models.Model):
    radionuclide_id = models.IntegerField(primary_key=True)
    radionuclide_name = models.CharField(max_length=50)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.radionuclide_name


class Language(models.Model):
    language_id = models.IntegerField(primary_key=True)
    language = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.language


class Reference(models.Model):
    ref_id = models.BigIntegerField(primary_key=True)
    author = models.CharField(max_length=500, null=True)
    article_title = models.CharField(max_length=500, null=True)
    pub_title = models.ForeignKey(PubTitle, on_delete=models.CASCADE, null=True)
    year = models.CharField(max_length=30, blank=True, null=True)
    volume = models.CharField(max_length=50, blank=True, null=True)
    part = models.CharField(max_length=50, blank=True, null=True)
    pages = models.CharField(max_length=50, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    pub_type = models.ForeignKey(PubType, on_delete=models.CASCADE, null=True)
    translation = models.BooleanField(default=False)
    notes = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    approval_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    approval_status = models.CharField(max_length=20, choices=approval_choices, default='PENDING', null=True, blank=True)

    def __str__(self):
        return self.article_title


class ReferenceRejectionReason(models.Model):
    reference = models.OneToOneField(Reference, on_delete=models.CASCADE, related_name='rejection_reason')
    reason = models.TextField()

    def __str__(self):
        return f"Rejection reason for {self.reference.article_title}"


class DataCR(models.Model):

    unit_choices = [ # both for media and for biota conc units
        ('µCi/kg', 'µCi/kg'),
        ('Bq/g', 'Bq/g'),
        ('Bq/kg', 'Bq/kg'),
        ('Bq/l', 'Bq/l'),
        ('Bq/m2', 'Bq/m2'),
        ('Bq/m3', 'Bq/m3'),
        ('mBq/g', 'mBq/g'),
        ('mBq/kg', 'mBq/kg'),
        ('mBq/l', 'mBq/l'),
        ('mg/g', 'mg/g'),
        ('mg/kg', 'mg/kg'),
        ('mg/l', 'mg/l'),
        ('pCi/g', 'pCi/g'),
        ('pCi/kg', 'pCi/kg'),
        ('pCi/l', 'pCi/l'),
        ('ppb', 'ppb'),
        ('ppm', 'ppm'),
        ('uCi/l', 'uCi/l'),
        ('ug/g', 'ug/g'),
        ('ug/kg', 'ug/kg'),
        ('ug/l', 'ug/l'),
    ]

    #cr_id = models.AutoField(primary_key=True)
    cr_id = models.BigIntegerField(primary_key=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)
    habitat = models.ForeignKey(Habitat, on_delete=models.CASCADE, null=True, blank=True)
    wildlife_group = models.ForeignKey(WildlifeGroup, on_delete=models.CASCADE, null=True, blank=True)
    icrp_rap = models.ForeignKey(RAP, on_delete=models.CASCADE, null=True, blank=True) # WildlifeGroup and RAP are different classification types -> mammal (deer, rat, horse) ↮ specifically deer, rat
    lifestage = models.ForeignKey(Lifestage, on_delete=models.CASCADE, null=True, blank=True)
    species_name = models.ForeignKey(SpeciesName, on_delete=models.CASCADE, null=True, blank=True)
    study_type = models.ForeignKey(StudyType, on_delete=models.CASCADE, null=True, blank=True)
    # goes to the end:
    measurement_date = models.CharField(max_length=50, null=True, blank=True)
    tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE, null=True, blank=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)
    # goes renamed:
    crn = models.IntegerField(null=True, blank=True) # how many times they did the calculation to get CR ("number of replicates")
    # goes renamed:
    cr = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    cr_sd = models.DecimalField(max_digits=25, decimal_places=10, null=True, blank=True) # standard deviation
    notes = models.CharField(max_length=500, null=True, blank=True)
    # goes up to other foreign keys
    radionuclide = models.ForeignKey(Radionuclide, on_delete=models.CASCADE, null=True, blank=True)
    # double?????? - delete!!!
    accepted = models.BooleanField(default=False)
    biohalflife = models.CharField(max_length=30, null=True, blank=True)
    biota_conc = models.CharField(max_length=30, null=True, blank=True)
    biota_conc_units = models.CharField(max_length=20, choices=unit_choices, null=True, blank=True)
    biota_n = models.IntegerField(null=True, blank=True)
    # goes implemented:
    biota_sd = models.CharField(max_length=30, null=True)
    biota_wet_dry_choices = [
        ('Water', 'Water'),
        ('Wet', 'Wet'),
        ('Dry', 'Dry'),
        ('Air', 'Air'),
        ('Soil', 'Soil'),
        ('undefined', 'undefined'),
    ]
    biota_wet_dry = models.CharField(max_length=20, choices=biota_wet_dry_choices, null=True, blank=True)
    # goes deleted:
    data_extract = models.IntegerField(null=True, blank=True)
    media_conc = models.CharField(max_length=30, null=True, blank=True)
    media_n = models.CharField(max_length=30, null=True, blank=True)
    media_conc_units = models.CharField(max_length=20, choices=unit_choices, null=True, blank=True)
    media_sd = models.CharField(max_length=30, null=True, blank=True)
    media_wet_dry_choices = [
        ('Water', 'Water'),
        ('Wet', 'Wet'),
        ('Dry', 'Dry'),
        ('Air', 'Air'),
        ('Soil', 'Soil'),
        ('undefined', 'undefined'),
    ]
    media_wet_dry = models.CharField(max_length=10, choices=media_wet_dry_choices, null=True, blank=True)
    # goes deleted:
    other_tissue = models.CharField(max_length=30, null=True, blank=True)
    # goes deleted:
    qc = models.BooleanField(default=False)
    rep_organ_units = models.CharField(max_length=30, null=True, blank=True)
    reproductive_organ = models.CharField(max_length=30, null=True, blank=True)
    rep_wet_dry_choices = [
        ('Water', 'Water'),
        ('Wet', 'Wet'),
        ('Dry', 'Dry'),
        ('Air', 'Air'),
        ('Soil', 'Soil'),
        ('undefined', 'undefined'),
    ]
    rep_wet_dry = models.CharField(max_length=10, choices=rep_wet_dry_choices, null=True, blank=True)
    # goes implemented:
    stand_biota_conc = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    stand_biota_sd = models.CharField(max_length=30, null=True, blank=True)
    stand_media_conc = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    stand_media_sd = models.CharField(max_length=30, null=True, blank=True)
    # goes deleted:
    summary_approve = models.BooleanField(default=False)
    approval_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    approval_status = models.CharField(max_length=20, choices=approval_choices, default='PENDING', null=True, blank=True)
