from rest_framework import viewsets, authentication, permissions, status, views, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .import serializers
from .import models
from.permissions import IsLecturer
from.venues_filter import get_available_venues, re_check_venues
# Create your views here.

class BaseAdminViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAdminUser, )

class CourseViewSet(BaseAdminViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    
class VenueViewSet(BaseAdminViewSet):
    queryset = models.Venue.objects.all()
    serializer_class = serializers.VenueSerializer

class SchoolTimetableViewSet(BaseAdminViewSet):
    queryset = models.SchoolTimetable.objects.all()
    serializer_class = serializers.SchoolTimetableSerializer

class UserScheduleViewset(viewsets.ModelViewSet):
    queryset = models.UserScheduledTimetable.objects.all()
    serializer_class = serializers.UserScheduledTimetableSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (IsLecturer, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-start_date_and_time')    

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
       

class ListAvailableVenuesView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = serializers.QueryParamsSerializer
    
    def post(self, request):
        serialized = serializers.QueryParamsSerializer(data=self.request.data)
        if serialized.is_valid(raise_exception=True):
            date = serialized.data['start_date_and_time'].date()
            start = serialized.data['start_date_and_time'].time()
            end = serialized.data['end_time']

            venues = get_available_venues(date=date, start=start, end=end)

            return Response({'available-venues':venues})      

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationView(generics.ListAPIView):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-created_at')