# Generated by Django 3.0.12 on 2021-03-01 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0026_auto_20210228_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zmatecne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_hlasovani', models.ForeignKey(db_column='id_hlasovani', on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Hl_Hlasovani')),
            ],
        ),
    ]