from rest_framework import viewsets,permissions, status, views, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, filters

from django.contrib.contenttypes.models import ContentType

from .import serializers
from .import models
from.permissions import CustomDjangoModelPermission
from.venues_filter import get_available_venues
# Create your views here.

class BaseAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission] 
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['start_date_and_time']

    def perform_create(self,serializer):
        instance = serializer.save()
        date = serializer.data['start_date_and_time'].date()
        start = serializer.data['start_date_and_time'].time()
        time = serializer.initial_data['end_time']
        venue = serializer.initial_data['venue'] 
        
        obj = self.queryset.get(pk=instance.id)
        
        models.SummaryTimetable.objects.create(start_date=date, start_time=start, end_time=time, content_object=obj, venue=venue)

    def perform_destroy(self,request):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        summary = models.SummaryTimetable.objects.get(content_type=content_type,object_id=instance.id)
        summary.delete()
        instance.delete()

class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code','department__name']
    
class VenueViewSet(viewsets.ModelViewSet):
    queryset = models.Venue.objects.all()
    serializer_class = serializers.VenueSerializer
    permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ExamTimetableViewSet(BaseAdminViewSet):
    queryset = models.ExamTimetable.objects.all()
    serializer_class = serializers.ExamTimetableSerializer
    search_fields = ['course__code']

class EventViewSet(BaseAdminViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    search_fields = ['name','venue__name']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission] 
        return [permission() for permission in permission_classes]

class SchoolTimetableViewSet(viewsets.ModelViewSet):
    queryset = models.SchoolTimetable.objects.all()
    serializer_class = serializers.SchoolTimetableSerializer
    permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['course__code','course__department__name','day']
    ordering_fields = ['day','start_time']

    def perform_create(self,serializer):
        instance = serializer.save()
        start_time = serializer.initial_data['start_time']
        end_time = serializer.initial_data['end_time']
        day = serializer.initial_data['day']
        venue = serializer.initial_data['venue']
        obj = self.queryset.get(pk=instance.id)

        models.SummaryTimetable.objects.create(start_time=start_time, end_time=end_time, day=day, content_object=obj, venue=venue )
    
    def perform_destroy(self,request):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        summary = models.SummaryTimetable.objects.get(content_type=content_type,object_id=instance.id)
        summary.delete()
        instance.delete()

class UserScheduleViewset(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin):
    queryset = models.UserScheduledTimetable.objects.all()
    permission_classes = (CustomDjangoModelPermission, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-start_date_and_time')    

    def perform_create(self,serializer):
        instance = serializer.save(user=self.request.user)
        date = serializer.data['start_date_and_time'].date()
        start = serializer.data['start_date_and_time'].time()
        time = serializer.initial_data['end_time']
        venue = serializer.initial_data['venue'] 
        
        obj = self.queryset.get(pk=instance.id)

        models.SummaryTimetable.objects.create(start_date=date, start_time=start, end_time=time, content_object=obj, venue=venue)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserScheduledDetailSerializer
        return serializers.UserScheduledTimetableSerializer

    def perform_destroy(self,request):
        instance = self.get_object()
        content_type = ContentType.objects.get_for_model(instance)
        summary = models.SummaryTimetable.objects.get(content_type=content_type,object_id=instance.id)
        summary.delete()
        instance.delete()
       

class ListAvailableVenuesView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.QueryParamsSerializer
    
    def post(self, request):
        serialized = serializers.QueryParamsSerializer(data=self.request.data)
        if serialized.is_valid(raise_exception=True):
            date = serialized.data['start_date_and_time'].date()
            start = serialized.data['start_date_and_time'].time()
            end = serialized.data['end_time']

            venues = get_available_venues(date_day=date, start=start, end=end)

            if venues:
                serializer =  serializers.VenueSerializer(venues, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'error':"No available venues"})      

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationView(generics.ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')