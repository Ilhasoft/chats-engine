from rest_framework import status
from rest_framework.exceptions import APIException

from chats.apps.api.v1.internal.rest_clients.flows_rest_client import FlowRESTClient
from chats.apps.rooms.models import Room


def update_custom_fields(room: Room, custom_fields_update: dict):
    room.custom_fields.update(custom_fields_update)
    room.save()


def update_flows_custom_fields(project, data, contact_id):
    response = FlowRESTClient().create_contact(
        project=project,
        data=data,
        contact_id=contact_id,
    )
    if response.status_code not in [status.HTTP_200_OK]:
        raise APIException(
            {
                "Detail": f"[{response.status_code}]\n"
                + f"Error updating custom fields on flows. Exception: {response.content}"
            },
        )


def get_editable_custom_fields_room(room_filter: dict) -> Room:
    try:
        room = Room.objects.get(**room_filter)
    except Room.DoesNotExist:
        raise APIException(detail="Active room not found.")

    if not room.queue.sector.can_edit_custom_fields:
        raise APIException(
            detail="Access denied! You can't edit custom fields in this sector."
        )

    return room