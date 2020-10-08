from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import UserSerializer, DepartmentSerializer, RoleSerializer
from .models import Department, Role
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
    permission_classes = (permissions.IsAdminUser, )

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAdminUser,)