from django.db import models

# Create your models here.
class DataTableIndex(models.Model):
    sourcename = models.CharField(db_column='sourceName', max_length=255)  # Field name made lowercase.
    date = models.DateTimeField(blank=True, null=True)
    targetname = models.CharField(db_column='targetName', primary_key=True, max_length=255)  # Field name made lowercase.
    user = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    filesize = models.BigIntegerField(db_column='fileSize', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data_table_index'
