# Generated by Django 5.0.2 on 2024-02-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingest", "0003_remove_ingestfromsource_summary_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingestfromsource",
            name="authors",
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name="ingestfromsource",
            name="title",
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
