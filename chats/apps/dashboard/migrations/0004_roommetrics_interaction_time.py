# Generated by Django 4.1.2 on 2022-12-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0003_alter_roommetrics_waiting_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="roommetrics",
            name="interaction_time",
            field=models.IntegerField(default=0, verbose_name="Room interaction time"),
        ),
    ]
