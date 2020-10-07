from django.urls import path

from rest_framework import routers

from .import views

app_name = 'accounts'

router = routers.SimpleRouter()
router.register('department', views.DepartmentViewSet)
router.register('role', views.RoleViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]

urlpatterns += router.urls