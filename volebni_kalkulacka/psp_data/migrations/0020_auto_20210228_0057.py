# Generated by Django 3.0.12 on 2021-02-27 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0019_auto_20210228_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hist',
            name='id_schuze',
            field=models.ForeignKey(db_column='id_schuze', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Schuze'),
        ),
    ]