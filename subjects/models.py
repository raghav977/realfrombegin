from django.db import models
from classes.models import Section,ClassRoom,Class_section
from django.core.exceptions import ValidationError

# Create your models here.
class Subject(models.Model):
    subject_name = models.CharField(max_length=70)
    credit_hours = models.IntegerField(null=True,blank=True)

class ClassSubject(models.Model):
    class_obj = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('class_obj', 'subject')

    def __str__(self):
        return f"{self.subject.name} assigned to {self.class_obj.name}"

class SectionSubjectTeacher(models.Model):

    section = models.ForeignKey(Section, on_delete=models.CASCADE,null=True)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey('accounts.teacher', on_delete=models.CASCADE,null=True)

    class Meta:
        unique_together = ('section', 'class_subject')

    def __str__(self):
        return f"{self.teacher.user.email} teaches {self.class_subject.subject.subject_name} to {self.section}"

    def clean(self):
        if not Class_section.objects.filter(
            class_room=self.class_subject.class_obj,
            section=self.section
        ).exists():
            raise ValidationError(
                f"Section '{self.section.name}' does not belong to Class '{self.class_subject.class_obj.name}'."
            )


