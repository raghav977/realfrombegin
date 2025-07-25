from django.shortcuts import render
from accounts.permissions import IsStaffOrPrincipal
# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from section.models import ClassTeacher
from section.serializers import ClassTeacherSerializer

class CreateClassTeacherView(ListCreateAPIView):
    permission_classes = [IsStaffOrPrincipal]
    queryset = ClassTeacher.objects.all()
    serializer_class = ClassTeacherSerializer
    
    
    