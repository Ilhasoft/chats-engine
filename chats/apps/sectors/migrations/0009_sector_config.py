# Generated by Django 4.1.2 on 2023-08-08 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sectors", "0008_sector_can_edit_custom_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="sector",
            name="config",
            field=models.JSONField(blank=True, null=True, verbose_name="config"),
        ),
    ]