# Generated by Django 3.0.12 on 2021-02-27 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0015_auto_20210228_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tisky',
            name='id_stav',
            field=models.ForeignKey(db_column='id_stav', on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Stavy'),
        ),
    ]
