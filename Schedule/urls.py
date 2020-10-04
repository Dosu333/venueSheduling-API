from django.urls import path, include

from rest_framework import routers

from .import views

app_name = 'Schedule'

router = routers.SimpleRouter()
router.register('courses', views.CourseViewSet)
router.register('venues', views.VenueViewSet)
router.register('timetable', views.SchoolTimetableViewSet)
router.register('allocated-venues', views.UserScheduleViewset)

urlpatterns = [
    path('available-venues/', views.ListAvailableVenuesView.as_view()),
    path('notifications/', views.NotificationView.as_view())
]

urlpatterns += router.urls