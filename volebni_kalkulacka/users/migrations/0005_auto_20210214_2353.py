# Generated by Django 3.0.12 on 2021-02-14 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210212_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]