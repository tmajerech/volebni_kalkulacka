# Generated by Django 3.0.12 on 2021-03-05 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0028_auto_20210301_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zarazeni',
            name='id_organ',
        ),
        migrations.AddField(
            model_name='zarazeni',
            name='id_of',
            field=models.ForeignKey(db_column='id_of', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Organy'),
        ),
    ]
