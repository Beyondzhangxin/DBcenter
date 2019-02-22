# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DataUserIndex(models.Model):
    id = models.AutoField(db_column='Id',verbose_name=u"用户id",primary_key=True)  # Field name made lowercase.
    targetname = models.CharField(db_column='targetName',verbose_name=u"文件名", max_length=255, blank=True, null=True)  # Field name made lowercase.
    ispublic = models.IntegerField(db_column='isPublic', verbose_name=u"是否公开",blank=True, null=True)  # Field name made lowercase.
    shareuser = models.IntegerField(db_column='shareUser', verbose_name=u"分享用户id",blank=True, null=True)  # Field name made lowercase.
    datagroupnum = models.IntegerField(db_column='dataGroupNum',verbose_name=u"数据组", blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'data_user_index'
