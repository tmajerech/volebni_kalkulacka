# Generated by Django 3.0.12 on 2021-03-14 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0031_hl_hlasovani_important'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hl_Hlasovani_rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(db_column='rating', decimal_places=2, max_digits=3)),
                ('id_hlasovani', models.ForeignKey(db_column='id_hlasovani', on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.Hl_Hlasovani')),
            ],
        ),
        migrations.DeleteModel(
            name='Hl_Hlasovani_important',
        ),
    ]