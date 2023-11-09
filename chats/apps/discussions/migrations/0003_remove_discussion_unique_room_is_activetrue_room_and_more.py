# Generated by Django 4.1.2 on 2023-11-09 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("discussions", "0002_discussion_unique_room_is_activetrue_room"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="discussion",
            name="unique_room_is_activetrue_room",
        ),
        migrations.RenameField(
            model_name="discussionmessage",
            old_name="sender",
            new_name="user",
        ),
    ]
