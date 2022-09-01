from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, pagination, viewsets, filters

from chats.apps.api.v1.msgs.filters import MessageFilter
from chats.apps.api.v1.external.msgs.serializers import MsgFlowSerializer
from chats.apps.msgs.models import Message as ChatMessage


class MessageFlowViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ChatMessage.objects.all()
    serializer_class = MsgFlowSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    permission_classes = []
    # pagination_class = pagination.PageNumberPagination  # Removed temporarily
    lookup_field = "uuid"

    # def create(self, request, *args, **kwargs):
    #     # TODO USE THE REQUEST.USER TO SET THE USER IN THE MESSAGE
    #     return super().create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save()
    #     serializer.instance.notify_room("create")

    # def perform_update(self, serializer):
    #     serializer.save()
    #     serializer.instance.notify_room("update")
