from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance.views import AttendanceViewSet

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]
