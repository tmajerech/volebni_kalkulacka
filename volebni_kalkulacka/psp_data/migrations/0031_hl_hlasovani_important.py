# Generated by Django 3.0.12 on 2021-03-13 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0030_auto_20210306_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hl_Hlasovani_important',
            fields=[
                ('hl_hlasovani_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='psp_data.Hl_Hlasovani')),
            ],
            bases=('psp_data.hl_hlasovani',),
        ),
    ]
