# Generated by Django 3.0.12 on 2021-03-19 22:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_show_results_publicly'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kalkulacka_answers',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='kalkulacka_results',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
