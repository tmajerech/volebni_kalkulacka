# Generated by Django 3.0.12 on 2021-03-14 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0034_auto_20210314_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hist',
            name='id_hlas',
            field=models.ForeignKey(db_column='id_hlas', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Hl_Hlasovani'),
        ),
    ]
