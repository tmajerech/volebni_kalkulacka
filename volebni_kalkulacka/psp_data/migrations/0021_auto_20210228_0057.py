# Generated by Django 3.0.12 on 2021-02-27 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0020_auto_20210228_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hist',
            name='datum',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
