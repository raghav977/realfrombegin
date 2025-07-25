# assignment/models.py
from django.db import models
from accounts.models import User, Teacher, Student
from subjects.models import Subject,SectionSubjectTeacher
from classes.models import Section

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher_subject_section = models.ForeignKey(SectionSubjectTeacher,on_delete=models.SET_NULL,null=True,blank=True)
    total_marks = models.PositiveIntegerField(default=100)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    submission_file = models.FileField(upload_to='submissions/')
    remarks = models.TextField(blank=True, null=True)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)
    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"

    class Meta:
        unique_together = ('assignment', 'student')