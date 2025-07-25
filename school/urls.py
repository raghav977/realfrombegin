from django.urls import path
from .views import CreateSchoolView, SchoolStatsView
# from .views import AddItemView
urlpatterns = [
    path('school/',CreateSchoolView.as_view()),
    # path('demo/',AddItemView.as_view()),

    path('stats/', SchoolStatsView.as_view(), name='school-stats'),

]
