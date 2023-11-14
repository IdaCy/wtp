from django.db import models


class Client(models.Model):
    ClientID = models.IntegerField(primary_key=True)
    Salutation = models.CharField(max_length=50)
    Firstname = models.CharField(max_length=200)
    Lastname = models.CharField(max_length=200)
    EmailAddress = models.CharField(max_length=200)
    JobTitle = models.CharField(max_length=200)
    CompanyName = models.CharField(max_length=200)
    CompanyStreet1 = models.CharField(max_length=200)
    CompanyStreet2 = models.CharField(max_length=200)
    CompanyCity = models.CharField(max_length=200)
    CompanyCountry = models.CharField(max_length=200)
    CompanyPostcode = models.CharField(max_length=50)
    CompanyTel = models.CharField(max_length=20)
    Website = models.CharField(max_length=200)
    CompanyFaxno = models.CharField(max_length=20)
    Username = models.CharField(max_length=50)
    Password1 = models.CharField(max_length=200)
    AdminPriv = models.BooleanField(default=False)
    MoreInfo = models.CharField(max_length=200)


class EditTable(models.Model):
    EditID = models.IntegerField(primary_key=True)
    TableName = models.CharField(max_length=50)


class Element(models.Model):
    ElementID = models.IntegerField(primary_key=True)
    Element = models.CharField(max_length=50)
    Approved = models.BooleanField(default=False)


class Habitat(models.Model):
    HabitatID = models.IntegerField(primary_key=True)
    Habitat = models.CharField(max_length=200)
    Approved = models.BooleanField(default=False)
    MainHabitatType = models.SmallIntegerField()
    UserID = models.IntegerField()


class Language(models.Model):
    LanguageID = models.IntegerField(primary_key=True)
    Language1 = models.CharField(max_length=50)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()


class Lifestage(models.Model):
    LifestageID = models.IntegerField(primary_key=True)
    Lifestage = models.CharField(max_length=50)
    Approved = models.BooleanField(default=False)
    LinktoRAP = models.IntegerField()


class Location(models.Model):
    LocationID = models.IntegerField(primary_key=True)
    Location = models.CharField(max_length=200)


class Media(models.Model):
    MediaID = models.IntegerField(primary_key=True)
    MediaType = models.CharField(max_length=50)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()
    HabitatID = models.IntegerField()


class PubTitle(models.Model):
    PubTitleID = models.IntegerField(primary_key=True)
    PubTitle = models.CharField(max_length=200)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()
    ArticleType = models.CharField(max_length=50)


class PubType(models.Model):
    PubTypeID = models.IntegerField(primary_key=True)
    ArticleType = models.CharField(max_length=200)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()


class SpeciesName(models.Model):
    SpeciesID = models.IntegerField(primary_key=True)
    NameLatin = models.CharField(max_length=200)
    NameCommon = models.CharField(max_length=200)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()


class StudyType(models.Model):
    StudyTypeID = models.IntegerField(primary_key=True)
    StudyType = models.CharField(max_length=50)


class Tissue(models.Model):
    TissueID = models.IntegerField(primary_key=True)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()
    CorrectionFactor = models.CharField(max_length=30)


class MaterialStatus(models.Model):
    MaterialStatusID = models.IntegerField(primary_key=True)
    MaterialStatus = models.CharField(max_length=50)
    CorrectionRatio = models.DecimalField(max_digits=10, decimal_places=3)
    MediaTypeID = models.ForeignKey(Media, on_delete=models.CASCADE)


class Wildlife(models.Model):
    WildlifeGroupNumber = models.IntegerField(primary_key=True)
    WildlifeGroup = models.CharField(max_length=200)
    Approved = models.BooleanField(default=False)
    HabitatID = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    DataExtract = models.IntegerField()
    UserID = models.IntegerField()
    HabitatName = models.CharField(max_length=200)
    de_tophab_topwild = models.IntegerField()
    de_tophab_indwild = models.IntegerField()
    de_indhab_topwild = models.IntegerField()
    de_indhab_indwild = models.IntegerField()


class ActivityConcentrationUnit(models.Model):
    ActivityConcUnitID = models.AutoField(primary_key=True)
    ActConcUnits = models.CharField(max_length=50)
    Approved = models.BooleanField(default=False)
    CorrectionFactor = models.DecimalField(max_digits=10, decimal_places=3)
    MediaTypeID = models.ForeignKey(Media, on_delete=models.CASCADE)
    UnitNumber = models.SmallIntegerField()


class ParCRCalc(models.Model):
    CF_ID = models.IntegerField(primary_key=True)
    WildlifeGroup = models.ForeignKey(Wildlife, on_delete=models.CASCADE)
    Tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    WetDryRatio = models.DecimalField(max_digits=3, decimal_places=2)
    AshRatio = models.DecimalField(max_digits=3, decimal_places=2)
    FRESHER_CHOICES = [
        ('F', 'Freshwater'),
        ('M', 'Marine'),
        ('T', 'Terrestrial'),
    ]
    IsFreMarTer = models.CharField(max_length=1, choices=FRESHER_CHOICES)


class MaterialCRCalc(models.Model):
    CF_ID = models.IntegerField(primary_key=True)
    Element = models.ForeignKey(Element, on_delete=models.CASCADE)
    Organism = models.CharField(max_length=50)
    Liver = models.CharField(max_length=50)
    Bone = models.CharField(max_length=50)
    Muscle = models.CharField(max_length=50)
    FRESHER_CHOICES = [
        ('F', 'Freshwater'),
        ('M', 'Marine'),
        ('T', 'Terrestrial'),
    ]
    IsFreMarTer = models.CharField(max_length=1, choices=FRESHER_CHOICES)


class Radionuclide(models.Model):
    RadionuclideNumber = models.IntegerField(primary_key=True)
    Radionuclide = models.CharField(max_length=50)
    Element = models.ForeignKey(Element, on_delete=models.CASCADE)
    Approved = models.BooleanField(default=False)
    UserID = models.IntegerField()


class RAP(models.Model):
    RAP_ID = models.IntegerField(primary_key=True)
    RAP = models.CharField(max_length=200)
    HabitatID = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    Approved = models.BooleanField(default=False)
    WildlifeID = models.ForeignKey(Wildlife, on_delete=models.CASCADE)
    Summary = models.CharField(max_length=200)


class Reference(models.Model):
    RefID = models.IntegerField(primary_key=True)
    Author = models.CharField(max_length=500)
    ArticleTitle = models.CharField(max_length=500)
    PubTitle = models.ForeignKey(PubTitle, on_delete=models.CASCADE)
    Year1 = models.SmallIntegerField()
    Volume = models.SmallIntegerField()
    Part = models.CharField(max_length=20)
    Pages = models.CharField(max_length=20)
    Language = models.ForeignKey(Language, on_delete=models.CASCADE)
    PubType = models.ForeignKey(PubType, on_delete=models.CASCADE)
    Translation1 = models.CharField(max_length=5)
    Keyword1 = models.CharField(max_length=50)
    Keyword2 = models.CharField(max_length=50)
    Keyword3 = models.CharField(max_length=50)
    Keyword4 = models.CharField(max_length=50)
    Location = models.CharField(max_length=200)
    Notes = models.CharField(max_length=500)
    UserID = models.IntegerField()
    DC_ID = models.IntegerField()
    ApprovalStatus = models.CharField(max_length=20)
    ReasonApprovalDelete = models.CharField(max_length=500)


class DataCR(models.Model):
    CR_ID = models.IntegerField(primary_key=True)
    RefID = models.ForeignKey(Reference, on_delete=models.CASCADE)
    HabitatID = models.ForeignKey(Habitat, on_delete=models.CASCADE)
    Wildlife = models.CharField(max_length=200)
    ICRPRAP = models.CharField(max_length=200)
    Lifestage = models.CharField(max_length=200)
    SpNameLatin = models.ForeignKey(SpeciesName, on_delete=models.CASCADE)
    StudyType = models.ForeignKey(StudyType, on_delete=models.CASCADE)
    MeasurementDate = models.DateField()
    Tissue = models.ForeignKey(Tissue, on_delete=models.CASCADE)
    Media = models.ForeignKey(Media, on_delete=models.CASCADE)
    CRN = models.SmallIntegerField()
    CR = models.IntegerField()
    CR_SD = models.IntegerField()
    Notes = models.CharField(max_length=500)
    Radionuclide = models.ForeignKey(Radionuclide, on_delete=models.CASCADE)
    FromERICA = models.BooleanField(default=False)
    Accepted = models.BooleanField(default=False)
    Biohalflife = models.CharField(max_length=30)
    BiotaConc = models.CharField(max_length=30)
    BiotaConcUnits = models.CharField(max_length=30)
    BiotaN = models.CharField(max_length=30)
    BiotaSD = models.CharField(max_length=30)
    BiotaWetDry = models.CharField(max_length=30)
    DataExtract = models.IntegerField()
    Location = models.CharField(max_length=30)
    MediaConc = models.CharField(max_length=30)
    MediaN = models.CharField(max_length=30)
    MediaConcUnits = models.CharField(max_length=30)
    MediaSD = models.CharField(max_length=30)
    MediaWetDry = models.CharField(max_length=30)
    OtherTissue = models.BooleanField(default=False)
    QC = models.CharField(max_length=30)
    RepOrganUnits = models.CharField(max_length=30)
    ReproductiveOrgan = models.CharField(max_length=30)
    RepWetDry = models.CharField(max_length=30)
    StandBiotaConc = models.CharField(max_length=30)
    StandBiotaSD = models.CharField(max_length=30)
    StandMediaConc = models.CharField(max_length=30)
    StandMediaSD = models.CharField(max_length=30)
    SummaryApprove = models.BooleanField(default=False)
    APPROVAL_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    ApprovalDataStatus = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='PENDING', )
