# Generated by Django 4.1.2 on 2022-12-14 13:14

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rooms", "0006_room_unique_contact_queue_is_activetrue_room"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoomMetrics",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(auto_now=True, verbose_name="Modified on"),
                ),
                (
                    "waiting_time",
                    models.IntegerField(default=0, verbose_name="Room Waiting time"),
                ),
                (
                    "queued_count",
                    models.IntegerField(default=0, verbose_name="Queued count"),
                ),
                (
                    "message_response_time",
                    models.IntegerField(
                        default=0, verbose_name="Messages response time"
                    ),
                ),
                (
                    "room",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="metric",
                        to="rooms.room",
                        verbose_name="Room Metric",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
