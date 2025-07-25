from django.urls import path
from section.views import CreateClassTeacherView
urlpatterns = [
    path('create/',CreateClassTeacherView.as_view(),name='class_teacher')
]
