# Generated by Django 3.0.12 on 2021-03-14 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0033_auto_20210314_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hl_hlasovani_rating',
            name='id',
        ),
        migrations.AlterField(
            model_name='hl_hlasovani_rating',
            name='id_hlasovani',
            field=models.OneToOneField(db_column='id_hlasovani', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='psp_data.Hl_Hlasovani'),
        ),
    ]
