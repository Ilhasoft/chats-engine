# Generated by Django 4.1.2 on 2024-03-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0010_alter_room_urn"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="protocol",
            field=models.TextField(
                blank=True, default="", null=True, verbose_name="protocol"
            ),
        ),
    ]