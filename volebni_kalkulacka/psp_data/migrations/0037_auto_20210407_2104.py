# Generated by Django 3.1.7 on 2021-04-07 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psp_data', '0036_auto_20210315_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='bod',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='cas',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='cislo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='datum',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='druh_hlasovani',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='id_organ',
            field=models.ForeignKey(db_column='id_organ', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='psp_data.organy'),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='kvorum',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='nehlasoval',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='prihlaseno',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='pro',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='proti',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='vysledek',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='hl_hlasovani',
            name='zdrzel',
            field=models.IntegerField(null=True),
        ),
    ]
