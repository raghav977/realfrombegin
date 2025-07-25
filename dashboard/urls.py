from django.urls import path
from .views import (
    TotalStudentsView,
    TotalTeachersView,
    StudentsListView,
    TeachersListView
)

urlpatterns = [
    path('stats/total-students/', TotalStudentsView.as_view(), name='total-students'),
    path('stats/total-teachers/', TotalTeachersView.as_view(), name='total-teachers'),
    path('stats/students/', StudentsListView.as_view(), name='students-list'),
    path('stats/teachers/', TeachersListView.as_view(), name='teachers-list'),
]