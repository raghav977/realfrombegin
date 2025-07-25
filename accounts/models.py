from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from cloudinary.models import CloudinaryField
from classes.models import Class_section

# from subjects.models import Subject
class BaseUser(models.Model):
    # date_of_birth = models.DateField(null=True,blank=True)
    profile_pic = CloudinaryField('image', blank=True, null=True)
    # address = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        abstract = True

# Role choices
class RoleChoice:
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    STAFF = 'staff'
    MODERATOR = 'moderator'
    PRINCIPAL = 'principal'
    
    
    ROLE = (
        ('admin', 'ADMIN'),
        ('teacher', 'TEACHER'),
        ('student', 'STUDENT'),
        ('staff', 'STAFF'),
        ('moderator', 'MODERATOR'),
        ('principal','PRINCIPAL')
    )


class MyUserManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_kwargs):
        if not email or not password:
            raise ValueError("You must have both email and password")

        valid_roles = [r[0] for r in RoleChoice.ROLE]
        if not role or role not in valid_roles:
            raise ValueError("Invalid role selection")
        email = self.normalize_email(email.lower())
        print("The email:",email)
        print("The password:", password)
        
        user = self.model(email=email, username=email, role=role, **extra_kwargs)
        user.set_password(password)
        # user.username=email
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_kwargs):
        extra_kwargs.setdefault("is_staff", True)
        extra_kwargs.setdefault("is_superuser", True)
        extra_kwargs.setdefault("is_active", True)
        return self.create_user(email, role="admin", password=password, **extra_kwargs)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=RoleChoice.ROLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyUserManager()


class Teacher(BaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_teacher")
    phone_number = models.CharField(max_length=10,null=True)
    # classes = models.ManyToManyField(ClassRoom, blank=True)
    # sections = models.ManyToManyField(Class_section, blank=True)
    # subject = models.ManyToManyField(Subject,blank=True)
    qualification = models.CharField(max_length=100,blank=True,null=True)
    degree_certificate = models.FileField(blank=True)
    salary = models.IntegerField(blank=True,null=True)
    joining_date = models.DateField(blank=True,null=True)
    # address = models.CharField(max_length=100,blank=True)

class TeacherSection(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    section = models.ForeignKey(Class_section,on_delete=models.CASCADE)
    pass
class Student(BaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_student")
    roll_no = models.IntegerField()
    # class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)

    section = models.ForeignKey(Class_section, on_delete=models.SET_NULL, null=True)

    # parents email field
    # section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)

    date_of_birth = models.DateField()

    class Meta:
        unique_together = ["user","section"]

class Staff(BaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_staff")
    phone_number = models.CharField(max_length=10,null=True)


class Principal(BaseUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="principal_profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    school = models.OneToOneField('school.School', on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Principal: {self.user.get_full_name()}"

