# models.py
from django.db import models
from subjects.models import SectionSubjectTeacher
from accounts.models import Student
from exam.models import Exam


class SubjectResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='subject_results')
    section_subject_teacher = models.ForeignKey(
        SectionSubjectTeacher, on_delete=models.CASCADE, related_name='subject_results'
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_results')

    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    pass_marks = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)

    grade = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        unique_together = ('exam', 'section_subject_teacher', 'student')


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    
    total_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    total_marks = models.DecimalField(max_digits=6, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10)
    gpa = models.FloatField()

    class Meta:
        unique_together = ('exam', 'student')
