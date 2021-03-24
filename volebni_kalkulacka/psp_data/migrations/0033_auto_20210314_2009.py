# Generated by Django 3.0.12 on 2021-03-14 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0032_auto_20210314_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='hl_hlasovani_rating',
            name='difference',
            field=models.DecimalField(db_column='difference', decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='hl_hlasovani_rating',
            name='user_rating_down',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='hl_hlasovani_rating',
            name='user_rating_up',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani_rating',
            name='rating',
            field=models.DecimalField(db_column='rating', decimal_places=2, max_digits=5),
        ),
    ]
