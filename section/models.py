from django.db import models
from classes.models import Class_section
# Create your models here.
class ClassTeacher(models.Model):
    teacher = models.ForeignKey('accounts.teacher',on_delete=models.SET_NULL,null=True,blank=True)
    section = models.OneToOneField(Class_section,on_delete=models.SET_NULL,null=True,blank=True)
    
    
    # def clean(self):
    #     from subjects.models import SectionSubjectTeacher,Class_section
    #     class_sections = Class_section.objects.filter(section=self.section)
        
    #     # checking ki tyo teacher le kunai subject padai raxaki xaina tyo section ma
    #     teacher_teaching_on_that_section = SectionSubjectTeacher.objects.filter(section=self.section)
    def __str__(self):
        
        return f"{self.teacher.user.first_name} is the class teacher of the {self.section.class_room.name} {self.section.section.name}"