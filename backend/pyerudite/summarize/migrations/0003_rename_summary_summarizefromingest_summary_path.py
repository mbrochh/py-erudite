# Generated by Django 5.0.2 on 2024-02-22 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("summarize", "0002_rename_coutput_cost_summarizefromingest_output_cost"),
    ]

    operations = [
        migrations.RenameField(
            model_name="summarizefromingest",
            old_name="summary",
            new_name="summary_path",
        ),
    ]