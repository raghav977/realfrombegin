"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('grade/', include('grade.urls')),
    # path('section/', include('section.urls')),
    # path('api/', include('grade.urls')),
    # path('api/', include('section.urls')),
    path('accounts/',include('accounts.urls')),
    
    path('create/',include('school.urls')),
    path('class/',include('classes.urls')),
    path('subject/',include('subjects.urls')),
    # path('exam/', include('exam.urls')),

    path('dashboard/', include('dashboard.urls')),


    path('class-teacher/',include('section.urls')),
    path('attendance/', include('attendance.urls')),
    path('assignment/',include('assignments.urls')),
    # path('result/', include('result.urls')),

]
