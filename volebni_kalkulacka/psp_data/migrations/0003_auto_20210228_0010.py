# Generated by Django 3.0.12 on 2021-02-27 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0002_auto_20210228_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bod_stav',
            name='id',
        ),
        migrations.AlterField(
            model_name='bod_stav',
            name='id_bod_stav',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
