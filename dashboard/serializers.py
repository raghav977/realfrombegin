from rest_framework import serializers
from accounts.models import Student, Teacher

class StudentSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='section.class_room.name',read_only=True)
    section_name = serializers.CharField(source='section.section.name',read_only=True)
    student_name = serializers.CharField(source='user.email')
    class Meta:
        model = Student
        fields = ['id', 'roll_no', 'section', 'date_of_birth','class_name','section_name','student_name']

class TeacherSerializer(serializers.ModelSerializer):
    teacher_email = serializers.CharField(source='user.email',read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'phone_number', 'qualification', 'joining_date','teacher_email']