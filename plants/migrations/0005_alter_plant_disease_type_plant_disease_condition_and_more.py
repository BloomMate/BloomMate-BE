# Generated by Django 4.2.5 on 2023-11-12 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0004_alter_plant_disease_type_plant_disease_condition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant_disease_type',
            name='plant_disease_condition',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plant_disease_type',
            name='plant_disease_symptom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
