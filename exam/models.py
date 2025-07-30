from django.db import models
from school.models import AcademicYear

# Create your models here.

class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.exam_name} ({self.academic_year})"