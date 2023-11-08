# Generated by Django 4.1.2 on 2023-11-22 22:00

import chats.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("queues", "0005_queue_config"),
        ("rooms", "0010_alter_room_urn"),
        ("projects", "0019_flowstart_contact_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discussion",
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
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="is deleted?"),
                ),
                (
                    "subject",
                    models.CharField(max_length=50, verbose_name="Subject Text"),
                ),
                (
                    "is_queued",
                    models.BooleanField(default=True, verbose_name="Is queued?"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is active?"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussions",
                        to=settings.AUTH_USER_MODEL,
                        to_field="email",
                        verbose_name="Created By",
                    ),
                ),
                (
                    "queue",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussions",
                        to="queues.queue",
                        verbose_name="Queue",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussions",
                        to="rooms.room",
                        verbose_name="Room",
                    ),
                ),
            ],
            options={
                "verbose_name": "Discussion",
                "verbose_name_plural": "Discussions",
            },
            bases=(models.Model, chats.core.models.WebSocketsNotifiableMixin),
        ),
        migrations.CreateModel(
            name="DiscussionMessage",
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
                ("text", models.TextField(blank=True, null=True, verbose_name="Text")),
                (
                    "discussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="discussions.discussion",
                        verbose_name="discussion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussion_messages",
                        to=settings.AUTH_USER_MODEL,
                        to_field="email",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
                "ordering": ["created_on"],
            },
            bases=(chats.core.models.WebSocketsNotifiableMixin, models.Model),
        ),
        migrations.CreateModel(
            name="DiscussionMessage",
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
                ("text", models.TextField(blank=True, null=True, verbose_name="Text")),
                (
                    "discussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="discussions.discussion",
                        verbose_name="discussion",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussion_messages",
                        to=settings.AUTH_USER_MODEL,
                        to_field="email",
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="DiscussionUser",
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
                    "role",
                    models.PositiveIntegerField(
                        choices=[(0, "Creator"), (1, "Admin"), (2, "Participant")],
                        default=2,
                        verbose_name="role",
                    ),
                ),
                (
                    "discussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="added_users",
                        to="discussions.discussion",
                        verbose_name="Discussion",
                    ),
                ),
                (
                    "permission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussion_users",
                        to="projects.projectpermission",
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Discussion User",
                "verbose_name_plural": "Discussions Users",
            },
        ),
        migrations.CreateModel(
            name="DiscussionMessageMedia",
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
                    "content_type",
                    models.CharField(max_length=300, verbose_name="Content Type"),
                ),
                (
                    "media_file",
                    models.FileField(
                        blank=True,
                        max_length=300,
                        null=True,
                        upload_to="discussionmedia/%Y/%m/%d/",
                        verbose_name="Media File",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="medias",
                        to="discussions.discussionmessage",
                        verbose_name="discussion message",
                    ),
                ),
            ],
            options={
                "verbose_name": "Discussion Message Media",
                "verbose_name_plural": "Discussion Message Medias",
            },
        ),
        migrations.AddConstraint(
            model_name="discussionuser",
            constraint=models.UniqueConstraint(
                fields=("permission", "discussion"),
                name="unique_permission_per_discussion",
            ),
        ),
        migrations.AddConstraint(
            model_name="discussion",
            constraint=models.UniqueConstraint(
                condition=models.Q(("is_active", True)),
                fields=("room",),
                name="unique_room_is_activetrue_discussion",
            ),
        ),
    ]
