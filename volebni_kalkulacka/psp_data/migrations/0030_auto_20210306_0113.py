# Generated by Django 3.0.12 on 2021-03-06 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0029_auto_20210306_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organy',
            name='organ_id_organ',
            field=models.ForeignKey(db_column='organ_id_organ', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Organy'),
        ),
    ]
