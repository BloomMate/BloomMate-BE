# Generated by Django 4.2.5 on 2023-10-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_rename_questioner_id_community_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='question_updated_date',
            field=models.DateField(auto_now=True),
        ),
    ]