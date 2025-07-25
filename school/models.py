import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class AcademicYear(models.Model):
    academic_year = models.CharField(
        max_length=5,
        unique=True,
        validators=[MinLengthValidator(4)]
    )

    def __str__(self):
        return self.academic_year


class School(models.Model):
    school_name = models.CharField(max_length=200)
    school_code = models.CharField(max_length=200, primary_key=True, editable=False)
    established_date = models.DateField()
    pan_no = models.CharField(unique=True,max_length=9,validators=[MinLengthValidator(9)])
    academic_year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE,null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def save(self, *args, **kwargs):
        if not self.school_code:
            numbser = str(self.pan_no)
            suffix = numbser[-1:-4:-1]  
            prefix = self.school_name[:3].upper()
            self.school_code = f"{prefix}-{suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.school_name

