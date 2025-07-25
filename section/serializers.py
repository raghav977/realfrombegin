from section.models import ClassTeacher
# from rest_framework.serializers import Serializer
from rest_framework import serializers
from subjects.models import SectionSubjectTeacher

class ClassTeacherSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='section.class_room.name',read_only=True)
    section_name = serializers.CharField(source='section.section.name',read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.email',read_only=True)
    class Meta:
        model = ClassTeacher
        fields = ['teacher','section','class_name','section_name','teacher_name']
    
    def validate(self,data):
        print("This is data",data)
        teacher = data.get('teacher')
        section = data.get('section')
        class_room = section.class_room

        if teacher and section:
            section_id = section.section
            # class_id = section.
            print("The section name is",section_id.name)
            print("The class name is",class_room.name)
            # aba check garne tyo teacher chai xa ki xaina tyo section ma
            teacher_exists_in_section = SectionSubjectTeacher.objects.filter(
                section=section_id,
                teacher=teacher,
                class_subject__class_obj=class_room
                ).exists()
            if not teacher_exists_in_section:
                raise serializers.ValidationError({
                        "teacher": "This teacher is not assigned to teach in this section's class."
                    })

            return data


