# Generated by Django 3.0.12 on 2021-02-28 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0022_auto_20210228_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hist',
            name='id_bod',
            field=models.IntegerField(null=True),
        ),
    ]
