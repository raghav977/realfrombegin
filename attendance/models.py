# # from django.db import models
# # from django.utils import timezone
# # from accounts.models import Teacher, Student
# # # from section.models import 
# # from classes.models import Class_section
# # from section.models import ClassTeacher
# # class Attendance(models.Model):
# #     # section = models.ForeignKey(Class_section, on_delete=models.CASCADE, related_name='attendances')
# #     # date = models.DateField(default=timezone.now)
# #     # taken_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='taken_attendances')
# #     # created_at = models.DateTimeField(auto_now_add=True)
# #     # updated_at = models.DateTimeField(auto_now=True)
# #     class_teacher = models.ForeignKey(ClassTeacher,on_delete=models.SET_NULL,null=True)
# #     student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
# #     # date = models.

# #     class Meta:
# #         # unique_together = ('section', 'date')
# #         # ordering = ['-date']
# #         pass

# #     # def __str__(self):
# #     #     return f"{self.section} - {self.date}"

# # class AttendanceRecord(models.Model):
# #     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='records')
# #     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
# #     STATUS_CHOICES = [
# #         ('present', 'Present'),
# #         ('absent', 'Absent'),
# #         ('late', 'Late'),
# #         ('excused', 'Excused'),
# #     ]
# #     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
# #     remarks = models.CharField(max_length=100, blank=True, null=True)

# #     class Meta:
# #         unique_together = ('attendance', 'student')

# #     def __str__(self):
# #         return f"{self.student} - {self.status}"



# from django.db import models
# from django.utils import timezone
# from accounts.models import Student
# from section.models import ClassTeacher

# class Attendance(models.Model):
#     # section = models.ForeignKey
#     class_teacher = models.ForeignKey(ClassTeacher, on_delete=models.SET_NULL, null=True)
#     date = models.DateField(default=timezone.now)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('class_teacher', 'date')
#         ordering = ['-date']

#     def __str__(self):
#         return f"{self.class_teacher} - {self.date}"


# class AttendanceRecord(models.Model):
#     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='records')
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')

#     STATUS_CHOICES = [
#         ('present', 'Present'),
#         ('absent', 'Absent'),
#         ('late', 'Late'),
#         ('excused', 'Excused'),
#     ]
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
#     remarks = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         unique_together = ('attendance', 'student')

#     def __str__(self):
#         return f"{self.student} - {self.attendance.date} - {self.status}"

from django.db import models
from section.models import ClassTeacher
from accounts.models import Student
from django.db import models
from section.models import ClassTeacher

class Attendance(models.Model):
    class_teacher = models.ForeignKey(ClassTeacher, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)  # Optional: or allow manual date
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_teacher} - {self.date}"

class StudentAttendance(models.Model):
    attendance = models.ForeignKey(Attendance, related_name='student_attendances', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.student} - {self.status}"