from rest_framework import permissions
from accounts.models import Role

class IsNotStudent(permissions.BasePermission):
    """ Checks if user is a lecturer"""

    def has_permission(self,request,view):
        student = Role.objects.get(name="student")
        return student not in request.user.role.all()