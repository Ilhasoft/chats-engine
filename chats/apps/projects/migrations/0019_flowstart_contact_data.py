# Generated by Django 4.1.2 on 2023-10-23 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0018_templatetype_project_is_template_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="flowstart",
            name="contact_data",
            field=models.JSONField(default=dict, verbose_name="contact data"),
        ),
    ]
