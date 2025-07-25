from django.urls import path
from .views import CreateClassWithSectionsView
urlpatterns=[
    path('classrooms/',CreateClassWithSectionsView.as_view()),
    
    # path('sections/',CreateClass.as_view()),
]