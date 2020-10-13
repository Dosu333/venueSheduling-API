from django.urls import path

from rest_framework import routers

from .import views

app_name = 'accounts'

router = routers.SimpleRouter()
router.register('department', views.DepartmentViewSet)
router.register('users', views.AdminManageUserViewSet)
router.register('roles', views.GroupViewSet)
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]

urlpatterns += router.urls