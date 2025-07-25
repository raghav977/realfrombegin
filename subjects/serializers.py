from rest_framework import serializers
from classes.models import Section,ClassRoom,Class_section
from accounts.models import Teacher
from subjects.models import Subject,ClassSubject,SectionSubjectTeacher

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']

class ClassSubjectSerializer(serializers.ModelSerializer):
    
    class_name = serializers.CharField(source='class_obj.name', read_only=True)
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    
    class_obj = serializers.PrimaryKeyRelatedField(queryset=ClassRoom.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = ClassSubject
        fields = ['id', 'class_obj', 'subject','class_name','subject_name']

class SectionSubjectTeacherSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())
    class_subject = serializers.PrimaryKeyRelatedField(queryset=ClassSubject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    section_name = serializers.CharField(source='section.name', read_only=True)
    class_name = serializers.CharField(source='class_subject.class_obj.name', read_only=True)
    subject_name = serializers.CharField(source='class_subject.subject.subject_name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.email', read_only=True)

    class Meta:
        model = SectionSubjectTeacher
        fields = [
            'id', 
            'section', 'section_name', 
            'class_subject', 'class_name', 'subject_name',
            'teacher', 'teacher_name'
        ]

    def validate(self, attrs):
        section = attrs.get('section')
        class_subject = attrs.get('class_subject')

        # Check if Class_section with this class and section exists
        if not Class_section.objects.filter(class_room=class_subject.class_obj, section=section).exists():
            raise serializers.ValidationError(
                f"Section '{section.name}' does not belong to Class '{class_subject.class_obj.name}'."
            )
        return attrs

