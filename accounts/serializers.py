


from rest_framework import serializers
from rolepermissions.roles import assign_role

from classes.models import Section
from .models import Staff, User, Teacher, Student, Principal,TeacherSection
from django.contrib.auth.hashers import make_password
from subjects.models import Subject


class StaffCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Staff
        fields = ['email', 'first_name', 'last_name', 'password',]

    def create(self, validated_data):
        # Extract user data
        user_data = {
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name', ''),
            'password': make_password(validated_data.pop('password')),
            'role': 'staff'
        }

        # Create user first
        user = User.objects.create_user(**user_data)

        # Then create staff profile
        staff = Staff.objects.create(user=user, **validated_data)

        return staff


class TeacherCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    # sections = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=Section.objects.all(),
    #     required=False
    # )
    # teacher = serializers.DictField()
    # section = serializers
    # section = serializers.
    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'password','phone_number']

    def create(self, validated_data):
        email = validated_data.pop('email')
      
        user_data = {
            'email': email,
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name', ''),
            'password': validated_data.pop('password'),
            'role': 'teacher',
        }
         
        user = User.objects.create_user(**user_data)
        # sections = validated_data.pop("sections", [])
        teacher = Teacher.objects.create(user=user,**validated_data)
        # teacher.sections.set(sections) 
        # print("This is validated_Data after sabai pop",validated_data)
        # teacher = Teacher.objects.create(user=user, **validated_data)
      
        
        # assign_role(user, 'teacher')
        return teacher

class TeacherSectionSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.email',read_only=True)
    class_name = serializers.CharField(source='section.class_room.name',read_only=True)
    section_name = serializers.CharField(source='section.section.name',read_only=True)
    class Meta:
        model = TeacherSection
        fields = ['teacher','section','teacher_name','class_name','section_name']
    pass
    
    
class TeacherReadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ['email', 'first_name', 'last_name', 'phone_number']


class StudentCreateSerializer(serializers.ModelSerializer):
    # print(Section.objects.filter(id=2))
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    
    section_name = serializers.CharField(source='section.section_name',read_only=True)
    class_name = serializers.CharField(source='section.class_name',read_only=True)
    # section = serializers.PrimaryKeyRelatedField()
    # section = serializers.PrimaryKeyRelatedField(
    #     queryset=Section.objects.all(),
    #     required=True
    # )
    # print(sectio)
    


    class Meta:
        model = Student
        fields = ['email', 'first_name', 'last_name', 'password',
                  'date_of_birth', 'roll_no', 'section','section_name','class_name']
                  

    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name', ''),
            'password': validated_data.pop('password'),
            'role': 'student'
        }
        user = User.objects.create_user(**user_data)
        # user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        # assign_role(user, 'student')
        return student


class PrincipalProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Principal
        fields = [
            'email', 'first_name', 'last_name', 'profile_pic',
            'phone_number', 'bio', 'joining_date', 'school_name'
        ]
        read_only_fields = ['email', 'joining_date', 'school_name']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update principal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class StaffProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Staff
        fields = [
            'email', 'first_name', 'last_name', 'profile_pic', 'phone_number'
        ]
        read_only_fields = ['email']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update staff fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class TeacherProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    sections = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Section.objects.all(),
        required=False
    )
    subject = serializers.PrimaryKeyRelatedField(many=True,queryset=Subject.objects.all(),required=False)

    class Meta:
        model = Teacher
        fields = [
            'email', 'first_name', 'last_name', 'profile_pic',
            'phone_number', 'qualification', 'sections',
            'degree_certificate', 'salary', 'joining_date','subject'
        ]
        read_only_fields = ['email', 'salary', 'joining_date']

    # def create(self,data):
    #     sections = data.pop("sections", [])
    #     teacher = Teacher.objects.create(**data)
    #     # teacher.sections.set(sections) 
    #     return teacher
    def update(self, instance, validated_data):
        print("This is instance",instance)
        print("This is validated data",validated_data)
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Handle sections update
        sections = validated_data.pop('sections', None)
        subjects = validated_data.pop('subjects',None)
        if sections is not None:
            instance.sections.set(sections)

        if subjects is not None:
            instance.subject.set(subjects)
        # Update teacher fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    section_name = serializers.CharField(source='section.name', read_only=True)
    grade_name = serializers.CharField(source='section.grade.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'email', 'first_name', 'last_name', 'profile_pic',
            'roll_no', 'date_of_birth', 'section', 'section_name', 'grade_name'
        ]
        read_only_fields = ['email', 'roll_no', 'section', 'section_name', 'grade_name']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update user fields
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
    
        # Update student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance