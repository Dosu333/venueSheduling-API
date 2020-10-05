from rest_framework import permissions

class IsLecturer(permissions.BasePermission):
    """ Checks if user is a lecturer"""

    def has_permission(self,request,view):
        return request.user.is_lecturer