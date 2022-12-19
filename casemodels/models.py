from django.db import models

# Create your models here.
class CaseDetails(models.Model):
    id = models.AutoField(primary_key=True)
    caseImage = models.FileField(upload_to='caseImage')
    caseName = models.CharField(max_length=25)
    caseRate = models.IntegerField()

    class Meta:
        db_table = "CaseDetails"


class DesignDetails(models.Model):
    id = models.AutoField(primary_key=True,)
    DesignImage = models.FileField(upload_to='DesignImage')
    DesignName = models.CharField(max_length=25)
    CaseName = models.CharField(max_length=25)
    
    class Meta:
        db_table = "DesignDetails"


class PhoneDetails(models.Model):
    id = models.AutoField(primary_key=True)
    PhoneName = models.CharField(max_length=25)

    class Meta:
        db_table = "PhoneDetails"