from django.urls import path
from accounts.views import GoogleLogin, PrincipalProfileView, PrincipalDeleteView, StaffLoginView, StaffProfileView, \
    StaffDeleteView,StudentLoginView
from accounts.views import GoogleLogin, CreateStaffView, CreateTeacherView, CreateStudentView,TeacherProfileView,TeacherLoginView,TeacherSection

urlpatterns = [
    path('login/',GoogleLogin.as_view()),
     path('staff/create/', CreateStaffView.as_view(), name='create-staff'),

    path('teacher/create/', CreateTeacherView.as_view(), name='create-teacher'),
    path('teacher/assign-section/',TeacherSection.as_view(),name='teacher-assign-section'),
    
    
    path('student/create/', CreateStudentView.as_view(), name='create-student'),
    path('student/login/',StudentLoginView.as_view(),name='student-login'),

    path('principal/profile/', PrincipalProfileView.as_view(), name='principal-profile'),
    path('principal/delete/', PrincipalDeleteView.as_view(), name='principal-delete'),

    path('staff/login/', StaffLoginView.as_view(), name='staff-login'),
    path('staff/profile/', StaffProfileView.as_view(), name='staff-profile'),
    path('staff/delete/', StaffDeleteView.as_view(), name='staff-delete'),
    
    path('teacher/profile/',TeacherProfileView.as_view(),name='teacher-profile'),
    path('teacher/login/',TeacherLoginView.as_view(),name='teacher-profile'),
    
]
