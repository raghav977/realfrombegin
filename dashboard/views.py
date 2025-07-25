from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.permissions import IsPrincipal
from .filters import StudentFilter, TeacherFilter
from .serializers import StudentSerializer, TeacherSerializer
from accounts.models import Student, Teacher
from django_filters.rest_framework import DjangoFilterBackend


class TotalStudentsView(GenericAPIView):
    permission_classes = [IsPrincipal]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    queryset = Student.objects.all()

    def get(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        return Response({
            'total_students': filtered_queryset.count()
        })


class TotalTeachersView(GenericAPIView):
    permission_classes = [IsPrincipal]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
    queryset = Teacher.objects.all()

    def get(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        return Response({
            'total_teachers': filtered_queryset.count()
        })


class StudentsListView(GenericAPIView):
    permission_classes = [IsPrincipal]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)


class TeachersListView(GenericAPIView):
    permission_classes = [IsPrincipal]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)