from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins, filters
from rest_framework.decorators import action


from .serializers import UserSerializer, DepartmentSerializer, AdminManageUserSerializer, GroupSerializer 
from .models import Department
from Schedule.permissions import CustomDjangoModelPermission
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """CREATE A NEW USER IN THE SYSTEM"""
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAdminUser|CustomDjangoModelPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]

class AdminManageUserViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin
                            ):
    queryset = get_user_model().objects.all()
    serializer_class = AdminManageUserSerializer
    permission_classes = (permissions.IsAdminUser, )
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name','department__name']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permissions_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['get',])
    def get_users(self, request, pk=None):
        users = get_user_model().objects.filter(groups__id=pk)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  

from Schedule.models import SummaryTimetable
from django.db.models import Q
from datetime import datetime
today = datetime.today()
now = datetime.now().time()
qs = SummaryTimetable.objects.filter(Q(start_date__lt=today) | (Q(start_date=today) & Q(end_time__lte=now)) )
# for items in qs:
#    items.content_object.delete()
#    items.delete()
print(qs.query)