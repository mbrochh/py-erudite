# Generated by Django 5.0.2 on 2024-02-13 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("summarize", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="summarizefromingest",
            old_name="coutput_cost",
            new_name="output_cost",
        ),
    ]
