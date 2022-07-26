from django.db import models
from django.forms import JSONField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from chats.core.models import BaseModel
from chats.utils.websockets import send_channels_group

# TODO: Use djongo(mongodb) models? Might change how things works


class Room(BaseModel):
    user = models.ForeignKey(
        "accounts.User",
        related_name="rooms",
        verbose_name=_("messages"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        "contacts.Contact",
        related_name="rooms",
        verbose_name=_("messages"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    sector = models.ForeignKey(
        "sectors.Sector",
        related_name="rooms",
        verbose_name=_("Sector"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    ended_at = models.DateTimeField(
        _("Ended at"), auto_now_add=False, null=True, blank=True
    )

    ended_by = models.CharField(_("Ended by"), max_length=50)

    is_active = models.BooleanField(_("is active?"), default=True)

    transfer_history = JSONField(_("Transfer History"))

    tags = models.ManyToManyField(
        "sectors.SectorTag",
        verbose_name=_("tags"),
        related_name="rooms",
    )

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    @property
    def serialized_ws_data(self):
        from chats.apps.api.v1.rooms.serializers import RoomSerializer  # noqa

        return RoomSerializer(self).data

    def close(self, tags=None, end_by: str = ""):
        self.is_active = False
        self.ended_at = timezone.now()
        self.ended_by = end_by
        for tag_id in tags:
            self.tags.add(tag_id)
        self.save()

    def notify_sector(self, action):
        """
        Used to notify channels groups when something happens on the instance.

        Actions:
        Create

        e.g.:
        Contact create new room,
        Call the sector group(all agents) and send the 'create' action to add them in the room group
        """

        send_channels_group(
            group_name=f"sector_{self.sector.pk}",
            type="notify",
            content=self.serialized_ws_data,
            action=f"rooms.{action}",
        )

    def notify_room(self, action):
        """
        Used to notify channels groups when something happens on the instance.

        Actions:
        Update, Delete

        e.g.:
        Agent enters room,
        Call the sector group(all agents) and send the 'update' action to remove them from the group
        """

        send_channels_group(
            group_name=f"room_{self.pk}",
            type="notify",
            content=self.serialized_ws_data,
            action=f"rooms.{action}",
        )
