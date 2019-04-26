# Generated by Django 2.1.4 on 2019-04-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataUserIndex',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('targetname', models.CharField(blank=True, db_column='targetName', max_length=255, null=True)),
                ('ispublic', models.IntegerField(blank=True, db_column='isPublic', null=True)),
                ('shareuser', models.IntegerField(blank=True, db_column='shareUser', null=True)),
                ('datagroupnum', models.IntegerField(blank=True, db_column='dataGroupNum', null=True)),
                ('allowed_space_size', models.IntegerField(blank=True, null=True)),
                ('used_space_size', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_user_index',
                'managed': False,
            },
        ),
    ]
