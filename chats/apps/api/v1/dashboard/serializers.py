from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from chats.apps.dashboard.models import RoomMetrics
from chats.apps.projects.models import Project, ProjectPermission
from chats.apps.queues.models import Queue, QueueAuthorization

from chats.apps.rooms.models import Room
from django.db.models import F, Sum, Count, Q

from chats.apps.sectors.models import Sector, SectorTag


class DashboardRoomsSerializer(serializers.ModelSerializer):

    active_chats = serializers.SerializerMethodField()
    interact_time = serializers.SerializerMethodField()
    response_time = serializers.SerializerMethodField()
    waiting_time = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "active_chats",
            "interact_time",
            "response_time",
            "waiting_time"
        ]

    def get_active_chats(self, project):
        return Room.objects.filter(queue__sector__project=project, is_active=True).count()

    def get_interact_time(self, project):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector__project=project).count()
        
        interaction = RoomMetrics.objects.filter(room__queue__sector__project=project).aggregate(interaction_time=Sum('interaction_time'))["interaction_time"]
        interaction_time = interaction/metrics_rooms_count

        return interaction_time

       
    def get_response_time(self, project):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector__project=project).count()
        
        room_metric = RoomMetrics.objects.filter(room__queue__sector__project=project).aggregate(message_response_time=Sum('message_response_time'))["message_response_time"]
        response_time = room_metric/metrics_rooms_count

        return response_time
        
    def get_waiting_time(self, project):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector__project=project).count()
        
        room_metric = RoomMetrics.objects.filter(room__queue__sector__project=project).aggregate(waiting_time=Sum('waiting_time'))["waiting_time"]
        response_time = room_metric/metrics_rooms_count

        return response_time


class DashboardAgentsSerializer(serializers.ModelSerializer):

    project_agents = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "project_agents",
        ]

    def get_project_agents(self, project):
        
        queue_auth = QueueAuthorization.objects.filter(queue__sector__project=project, queue__sector__project__permissions__status="OFFLINE").values(
            "permission__user__first_name").annotate(
            count=Count("queue__rooms", filter=Q(queue__rooms__is_active=True), distinct=True))      

        return queue_auth


class DashboardSectorSerializer(serializers.ModelSerializer):

    sectors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "sectors",
        ]

    def get_sectors(self, project):
        sector = Sector.objects.filter(project=project).values(
            "name").annotate(
                waiting_time=Sum("queues__rooms__metric__waiting_time")/Count("queues__rooms__metric"), 
                response_time=Sum("queues__rooms__metric__message_response_time")/Count("queues__rooms__metric"),
                interact_time=Sum("queues__rooms__metric__interaction_time")/Count("queues__rooms__metric"),
                online_agents=(Count("project__permissions__status", filter=Q(project__permissions__status="ONLINE"), distinct=True))
            )
        return sector


class DashboardTagRoomFilterSerializer(serializers.ModelSerializer):

    total_rooms_tag = serializers.SerializerMethodField()
    interact_time_rooms_tag = serializers.SerializerMethodField()
    response_time_rooms_tag = serializers.SerializerMethodField()
    waiting_time_rooms_tag = serializers.SerializerMethodField()

    class Meta:
        model = SectorTag
        fields = [
            "total_rooms_tag",
            "interact_time_rooms_tag",
            "response_time_rooms_tag",
            "waiting_time_rooms_tag"
        ]
        
    def get_total_rooms_tag(self, sector_tag):
        tag_rooms = Room.objects.filter(queue__sector=sector_tag.sector).count()
        return tag_rooms


    def get_interact_time_rooms_tag(self, sector_tag):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).count()
        interaction = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).aggregate(interaction_time=Sum('interaction_time'))["interaction_time"]
        
        if interaction:
            interaction_time = interaction/metrics_rooms_count
        else:
            interaction_time = 0

        return interaction_time

    
    def get_response_time_rooms_tag(self, sector_tag):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).count()
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).aggregate(message_response_time=Sum('message_response_time'))["message_response_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time


    def get_waiting_time_rooms_tag(self, sector_tag):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).count()
        
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector_tag.sector).aggregate(waiting_time=Sum('waiting_time'))["waiting_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time


class DashboardTagAgentFilterSerializer(serializers.ModelSerializer):

    agent_tags = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = [
            "agent_tags",
        ]

    def get_agent_tags(self, sector_tag):
        agents_rooms_tags = Room.objects.filter(tags=sector_tag, is_active=True).values(
            "user").annotate(
            count=Count("tags"))      
        return agents_rooms_tags


class DashboardTagSectorFilterSerializer(serializers.ModelSerializer):

    sectors = serializers.SerializerMethodField()

    class Meta:
        model = SectorTag
        fields = [
            "sectors",
        ]

    def get_sectors(self, sector_tag):
        sector = Sector.objects.filter(uuid=sector_tag.sector.uuid, tags__name=sector_tag.name).values(
            "name").annotate(
                waiting_time=Sum("queues__rooms__metric__waiting_time")/Count("queues__rooms__metric"), 
                response_time=Sum("queues__rooms__metric__message_response_time")/Count("queues__rooms__metric"),
                interact_time=Sum("queues__rooms__metric__interaction_time")/Count("queues__rooms__metric"),
                online_agents=(Count("project__permissions__status", filter=Q(project__permissions__status="ONLINE"), distinct=True))
            )
        return sector


class DashboardSectorFilterSerializer(serializers.ModelSerializer):
    total_rooms_sector = serializers.SerializerMethodField()
    interact_time_rooms_sector = serializers.SerializerMethodField()
    response_time_rooms_sector = serializers.SerializerMethodField()
    waiting_time_rooms_sector = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "total_rooms_sector",
            "interact_time_rooms_sector",
            "response_time_rooms_sector",
            "waiting_time_rooms_sector"
        ]
        

    def get_total_rooms_sector(self, sector):
        sector_rooms = Room.objects.filter(queue__sector=sector).count()
        return sector_rooms


    def get_interact_time_rooms_sector(self, sector):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector).count()
        interaction = RoomMetrics.objects.filter(room__queue__sector=sector.sector).aggregate(interaction_time=Sum('interaction_time'))["interaction_time"]
        
        if interaction:
            interaction_time = interaction/metrics_rooms_count
        else:
            interaction_time = 0

        return interaction_time

    
    def get_response_time_rooms_sector(self, sector):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector).count()
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector.sector).aggregate(message_response_time=Sum('message_response_time'))["message_response_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time

    
    def get_waiting_time_rooms_sector(self, sector):
        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector.sector).count()
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector.sector).aggregate(waiting_time=Sum('waiting_time'))["waiting_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time
        

class DashboardSectorAgentFilterSerializer(serializers.ModelSerializer):

    agent_sector = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = [
            "agent_sector",
        ]

    def get_agent_sector(self, sector):
        agents_sector = QueueAuthorization.objects.filter(queue__sector=sector, queue__sector__project__permissions__status="OFFLINE").values(
            "permission__user__first_name").annotate(
            count=Count("queue__rooms", filter=Q(queue__rooms__is_active=True), distinct=True)) 

        return agents_sector


class DashboardSectorQueueFilterSerializer(serializers.ModelSerializer):

    queues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "queues",
        ]

    def get_queues(self, sector):
        queues = Queue.objects.filter(sector=sector).values(
            "name").annotate(
                waiting_time=Sum("rooms__metric__waiting_time")/Count("rooms__metric"), 
                response_time=Sum("rooms__metric__message_response_time")/Count("rooms__metric"),
                interact_time=Sum("rooms__metric__interaction_time")/Count("rooms__metric"),
                online_agents=(Count("sector__project__permissions__status", filter=Q(sector__project__permissions__status="OFFLINE"), distinct=True)),
            )
            
        return queues


class DashboardDateSectorFilterSerializer(serializers.ModelSerializer):
    total_rooms_sector = serializers.SerializerMethodField()
    interact_time_rooms_sector = serializers.SerializerMethodField()
    response_time_rooms_sector = serializers.SerializerMethodField()
    waiting_time_rooms_sector = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "total_rooms_sector",
            "interact_time_rooms_sector",
            "response_time_rooms_sector",
            "waiting_time_rooms_sector"
        ]
        

    def get_total_rooms_sector(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        sector_rooms = Room.objects.filter(queue__sector=sector, created_on__range=[start_date, end_date]).count()

        return sector_rooms

    def get_interact_time_rooms_sector(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector, room__created_on__range=[start_date, end_date]).count()
        interaction = RoomMetrics.objects.filter(room__queue__sector=sector, room__created_on__range=[start_date, end_date]).aggregate(interaction_time=Sum('interaction_time'))["interaction_time"]
        
        if interaction:
            interaction_time = interaction/metrics_rooms_count
        else:
            interaction_time = 0

        return interaction_time

    def get_response_time_rooms_sector(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector, room__created_on__range=[start_date, end_date]).count()
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector).aggregate(message_response_time=Sum('message_response_time'))["message_response_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time

    def get_waiting_time_rooms_sector(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        metrics_rooms_count = RoomMetrics.objects.filter(room__queue__sector=sector, room__created_on__range=[start_date, end_date]).count()
        room_metric = RoomMetrics.objects.filter(room__queue__sector=sector, room__created_on__range=[start_date, end_date]).aggregate(waiting_time=Sum('waiting_time'))["waiting_time"]

        if room_metric:
            response_time = room_metric/metrics_rooms_count
        else:
            response_time = 0

        return response_time


class DashboardDateAgentsFilterSerializer(serializers.ModelSerializer):

    project_agents = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "project_agents",
        ]

    def get_project_agents(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")
        
        queue_auth = QueueAuthorization.objects.filter(queue__sector=sector, queue__sector__project__permissions__status="OFFLINE", created_on__range=[start_date, end_date]).values(
            "permission__user__first_name").annotate(
            count=Count("queue__rooms", filter=Q(queue__rooms__is_active=True), distinct=True))
        return queue_auth


class DashboardDateSectorSerializer(serializers.ModelSerializer):

    sectors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "sectors",
        ]

    def get_sectors(self, sector):
        start_date = self.context.get("start_date")
        end_date = self.context.get("end_date")

        queues = Queue.objects.filter(sector=sector, created_on__range=[start_date, end_date]).values(
            "name").annotate(
                waiting_time=Sum("rooms__metric__waiting_time")/Count("rooms__metric"), 
                response_time=Sum("rooms__metric__message_response_time")/Count("rooms__metric"),
                interact_time=Sum("rooms__metric__interaction_time")/Count("rooms__metric"),
                online_agents=(Count("sector__project__permissions__status", filter=Q(sector__project__permissions__status="OFFLINE"), distinct=True)),
            )
        return queues
        