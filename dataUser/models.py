# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DataUserIndex(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    targetname = models.CharField(db_column='targetName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='isPublic', blank=True, null=True)  # Field name made lowercase.
    shareuser = models.IntegerField(db_column='shareUser', blank=True, null=True)  # Field name made lowercase.
    datagroupnum = models.IntegerField(db_column='dataGroupNum', blank=True, null=True)  # Field name made lowercase.
    allowed_space_size = models.IntegerField(blank=True, null=True)
    used_space_size = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_user_index'

