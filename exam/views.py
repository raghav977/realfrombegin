from rest_framework import viewsets
from .models import Exam
from .serializers import ExamSerializer
from accounts.permissions import IsPrincipal

class ExamViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing exam instances.
    """
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()
    permission_classes = [IsPrincipal]