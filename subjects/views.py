from rest_framework import viewsets
from .models import  Section, Subject,  ClassSubject, SectionSubjectTeacher
from .serializers import (
      SubjectSerializer,
    TeacherSerializer, ClassSubjectSerializer, SectionSubjectTeacherSerializer
)
from accounts.models import Teacher
from classes.models import ClassRoom,Section
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStaffOrPrincipal
# class ClassViewSet(viewsets.ModelViewSet):
#     queryset = ClassRoom.objects.all()
#     serializer_class = ClassSerializer

# class SectionViewSet(viewsets.ModelViewSet):
#     queryset = Section.objects.all()
#     serializer_class = SectionSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ClassSubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer

class SectionSubjectTeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrPrincipal]
    queryset = SectionSubjectTeacher.objects.all()
    serializer_class = SectionSubjectTeacherSerializer
