from django.urls import path,include

from rest_framework import routers
from result.views import SubjectResultView,ExamResultView


urlpatterns = [
    path('marks/',SubjectResultView.as_view()),
    
    # yo chai admin athawa staff ya principal le access garna milne
    path('<int:class_section_id>/',ExamResultView.as_view())
    
]
