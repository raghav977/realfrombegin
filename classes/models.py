from django.db import models
# from accounts.models import Teacher,Student
# class Assignment(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     assigned_by = models.ForeignKey('accounts.Teacher', on_delete=models.CASCADE)
#     due_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class AssignmentStatus(models.Model):
#     assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
#     student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
#     submitted = models.BooleanField(default=False)
#     submission_date = models.DateTimeField(null=True, blank=True)
#     grade = models.CharField(max_length=10, blank=True)

#     def __str__(self):
#         return f"{self.student} - {self.assignment}"


# class Attendance(models.Model):
#     student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
#     recorded_by = models.ForeignKey('accounts.Teacher', on_delete=models.SET_NULL, null=True)

#     class Meta:
#         unique_together = ('student', 'date')

#     def __str__(self):
#         return f"{self.student} - {self.date} - {self.status}"


# class Exam(models.Model):
#     EXAM_TYPE_CHOICES = [
#         ('Terminal', 'Terminal'),
#         ('Final', 'Final'),
#     ]

#     name = models.CharField(max_length=100)
#     exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.name} ({self.exam_type})"


# class ExamResult(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
#     subject = models.CharField(max_length=100)
#     marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
#     total_marks = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return f"{self.student} - {self.subject} - {self.exam}"


class ClassRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Grade 10", "Class 8"

    def __str__(self):
        return self.name


class Section(models.Model):
   name = models.CharField(max_length=100) 
#    esma chai section ko name eg: A,B,C

class Class_section(models.Model):
    class_room = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    
    # esma chai classroom ra section ko pk
