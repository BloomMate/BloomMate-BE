# Generated by Django 4.2.5 on 2023-11-10 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('article_title', models.CharField(max_length=255)),
                ('article_content_url', models.CharField(max_length=255)),
                ('article_thumbnail_url', models.CharField(max_length=255)),
            ],
        ),
    ]
