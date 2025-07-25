# assignment/urls.py
from django.urls import path
from .views import (
    AssignmentListCreateView,
    AssignmentDetailView,
    PublishAssignmentView,
    StudentAssignmentListView,
    AssignmentSubmissionCreateView,
    TeacherSubmissionListView,
    GradeSubmissionView,
    StudentSubmissionListView
)

urlpatterns = [
    # Teacher endpoints
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignments/<int:pk>/publish/', PublishAssignmentView.as_view(), name='publish-assignment'),
    path('assignments/<int:assignment_id>/submissions/', TeacherSubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view(), name='grade-submission'),

    # Student endpoints
    path('student/assignments/', StudentAssignmentListView.as_view(), name='student-assignment-list'),
    path('assignments/<int:assignment_id>/submit/', AssignmentSubmissionCreateView.as_view(), name='submit-assignment'),
    path('student/submissions/', StudentSubmissionListView.as_view(), name='student-submission-list'),
]