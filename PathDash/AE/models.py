from __future__ import unicode_literals

from django.db import models

class Attendance(models.Model):
    attendanceno = models.CharField(db_column='AttendanceNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    patientid = models.CharField(db_column='PatientID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    age = models.CharField(db_column='Age', max_length=10, blank=True, null=True)  # Field name made lowercase.
    episodedate = models.CharField(db_column='EpisodeDate', max_length=27, blank=True, null=True)  # Field name made lowercase.
    dischargetype = models.CharField(db_column='DischargeType', max_length=50, blank=True, null=True)  # Field name made lowercase.
    arrivaltype = models.CharField(db_column='ArrivalType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    plannedorunplanned = models.CharField(db_column='Plannedorunplanned', max_length=10, blank=True, null=True)  # Field name made lowercase.
    patientgroup = models.CharField(db_column='PatientGroup', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=10, blank=True, null=True)  # Field name made lowercase.
    timeinae = models.CharField(max_length=10, blank=True, null=True)
    hospitalsite = models.CharField(db_column='HospitalSite', max_length=10, blank=True, null=True)  # Field name made lowercase.
    consultantcode = models.CharField(max_length=10, blank=True, null=True)
    attendingclinician = models.CharField(db_column='AttendingClinician', max_length=10, blank=True, null=True)  # Field name made lowercase.
    consultingclinician1 = models.CharField(db_column='ConsultingClinician1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    consultingclinician2 = models.CharField(db_column='ConsultingClinician2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    triagenurse = models.CharField(db_column='TriageNurse', max_length=10, blank=True, null=True)  # Field name made lowercase.
    presentingcomplaint = models.CharField(db_column='PresentingComplaint', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription1 = models.CharField(db_column='DiagnosisDescription1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode1 = models.CharField(db_column='DiagnosisCode1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription2 = models.CharField(db_column='DiagnosisDescription2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode2 = models.CharField(db_column='DiagnosisCode2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription3 = models.CharField(db_column='DiagnosisDescription3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode3 = models.CharField(db_column='DiagnosisCode3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription4 = models.CharField(db_column='DiagnosisDescription4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode4 = models.CharField(db_column='DiagnosisCode4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription5 = models.CharField(db_column='DiagnosisDescription5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode5 = models.CharField(db_column='DiagnosisCode5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    diagnosisdescription6 = models.CharField(db_column='DiagnosisDescription6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    diagnosiscode6 = models.CharField(db_column='DiagnosisCode6', max_length=10, blank=True, null=True)  # Field name made lowercase.
    investigation1 = models.CharField(db_column='Investigation1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    investigation2 = models.CharField(db_column='Investigation2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    investigation3 = models.CharField(db_column='Investigation3', max_length=100, blank=True, null=True)  # Field name made lowercase.
    investigation4 = models.CharField(db_column='Investigation4', max_length=100, blank=True, null=True)  # Field name made lowercase.
    investigation5 = models.CharField(db_column='Investigation5', max_length=100, blank=True, null=True)  # Field name made lowercase.
    investigation6 = models.CharField(db_column='Investigation6', max_length=100, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis1 = models.CharField(db_column='LocalDiagnosis1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis2 = models.CharField(db_column='LocalDiagnosis2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis3 = models.CharField(db_column='LocalDiagnosis3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis4 = models.CharField(db_column='LocalDiagnosis4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis5 = models.CharField(db_column='LocalDiagnosis5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    localdiagnosis6 = models.CharField(db_column='LocalDiagnosis6', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attendance'
		
class Notes(models.Model):
    notesid = models.AutoField(db_column='NotesID', primary_key=True)  # Field name made lowercase.
    attendanceno = models.CharField(db_column='AttendanceNo', max_length=10)  # Field name made lowercase.
    date = models.CharField(max_length=10, blank=True, null=True)
    note = models.TextField(blank=True, null=True)  # This field type is a guess.
    noteseq = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notes'


class Tests(models.Model):
    testid = models.AutoField(db_column='TestID', primary_key=True)  # Field name made lowercase.
    attendanceno = models.CharField(db_column='AttendanceNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    patientid = models.CharField(db_column='PatientID', max_length=20)  # Field name made lowercase.
    datereceived = models.CharField(max_length=27, blank=True, null=True)
    datebookedin = models.CharField(max_length=27, blank=True, null=True)
    specimen_number = models.CharField(max_length=14)
    clindetails = models.CharField(db_column='ClinDetails', max_length=120, blank=True, null=True)  # Field name made lowercase.
    set_code = models.CharField(max_length=6)
    set_exp = models.CharField(max_length=20, blank=True, null=True)
    specimen_taken_by = models.CharField(max_length=20, blank=True, null=True)
    consultant = models.CharField(max_length=21, blank=True, null=True)
    location = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tests'
