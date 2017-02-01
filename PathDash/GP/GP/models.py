# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Cost(models.Model):
    set_code = models.CharField(db_column='Set_code', max_length=25)  # Field name made lowercase.
    set_exp = models.CharField(db_column='Set_Exp', max_length=255, blank=True, null=True)  # Field name made lowercase.
    discipline = models.CharField(db_column='Discipline', max_length=25, blank=True, null=True)  # Field name made lowercase.
    internal_recharge = models.DecimalField(db_column='Internal_Recharge', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cost'


class Gptests(models.Model):
    testid = models.AutoField(db_column='TestID', primary_key=True)  # Field name made lowercase.
    patientid = models.CharField(db_column='PatientID', max_length=20)  # Field name made lowercase.
    datecollected = models.CharField(max_length=27, blank=True, null=True)
    datereceived = models.CharField(max_length=27, blank=True, null=True)
    datebookedin = models.CharField(max_length=27, blank=True, null=True)
    dateauthorised = models.CharField(max_length=27, blank=True, null=True)
    specimen_number = models.CharField(max_length=14)
    clindetails = models.CharField(db_column='ClinDetails', max_length=250, blank=True, null=True)  # Field name made lowercase.
    set_code = models.CharField(max_length=10)
    set_exp = models.CharField(max_length=20, blank=True, null=True)
    specimen_taken_by = models.CharField(max_length=20, blank=True, null=True)
    consultant = models.CharField(max_length=21, blank=True, null=True)
    location = models.CharField(max_length=10, blank=True, null=True)
    discipline = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'GPtests'

class Location(models.Model):
    location_code = models.CharField(max_length=10)
    location_exp = models.CharField(max_length=25, blank=True, null=True)
    patient_category_code = models.CharField(max_length=2, blank=True, null=True)
    unit_location_group_exp = models.CharField(max_length=26, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'