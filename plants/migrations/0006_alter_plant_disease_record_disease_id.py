# Generated by Django 4.2.5 on 2023-11-13 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0005_alter_plant_disease_type_plant_disease_condition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant_disease_record',
            name='disease_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='plants.plant_disease_type'),
        ),
    ]