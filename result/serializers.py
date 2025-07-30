# from rest_framework import serializers
# from result.models import SubjectResult
# from utils.helper_fun import check_class_section_exist
# class SubjectExamResultSerializer(serializers.ModelSerializer):
#     teacher_name = serializers.CharField(source='section_subject_teacher.teacher.user.email', read_only=True)
#     subject_name = serializers.CharField(source='section_subject_teacher.class_subject.subject.subject_name', read_only=True)
#     student_name = serializers.CharField(source='student.user.email', read_only=True)
#     class_name = serializers.CharField(source='section_subject_teacher.class_subject.class_obj.name', read_only=True)
#     section_name = serializers.CharField(source='section_subject_teacher.section.name', read_only=True)

#     class Meta:
#         model = SubjectResult
#         fields = [
#             'section_subject_teacher', 'student', 'obtained_marks', 'total_marks', 'pass_marks',
#             'student_name', 'class_name', 'teacher_name', 'subject_name', 'section_name'
#         ]

#     def validate(self, data):
#         # Add any validation logic here if needed
#         print("The data is", data)
#         section_teacher_subject = data.get('section_subject_teacher')
#         for data in data:
            
#             student = data.get('student')
#             student_class = student.section.class_room
            
#             student_section = student.section.section
            
#             result_class = section_teacher_subject.class_subject.class_obj
#             result_section = section_teacher_subject.section
            
#             exists = check_class_section_exist(result_class,result_section)
#             if not exists:
#                 return serializers.ValidationError({"error":"No class with this section exists"})
#             # student_section_exists

            
            
#             if(student_class !=result_class and student_section!=result_section):
#                 return serializers.ValidationError({f"Error":"This student -{student.user.email} does not belong to the class- {result_class.naname}, Section- {result_section.name}"})
                
                
#             return data

#     def create(self, validated_data):
#         print("The created", validated_data)
#         return []
#         # return SubjectResult.objects.create(**validated_data)

from rest_framework import serializers
from result.models import SubjectResult
from utils.helper_fun import check_class_section_exist

class SubjectExamResultSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='section_subject_teacher.teacher.user.email', read_only=True)
    subject_name = serializers.CharField(source='section_subject_teacher.class_subject.subject.subject_name', read_only=True)
    student_name = serializers.CharField(source='student.user.email', read_only=True)
    class_name = serializers.CharField(source='section_subject_teacher.class_subject.class_obj.name', read_only=True)
    section_name = serializers.CharField(source='section_subject_teacher.section.name', read_only=True)

    class Meta:
        model = SubjectResult
        fields = [
            'section_subject_teacher', 'student', 'obtained_marks', 'total_marks', 'pass_marks',
            'student_name', 'class_name', 'teacher_name', 'subject_name', 'section_name'
        ]

    def validate(self, data):
        section_teacher_subject = data.get('section_subject_teacher')
        student = data.get('student')

        # Get student's class and section
        student_class = student.section.class_room
        student_section = student.section.section

        # Get the class and section from subject teacher relation
        result_class = section_teacher_subject.class_subject.class_obj
        result_section = section_teacher_subject.section

        # Check if class-section exists
        exists = check_class_section_exist(result_class, result_section)
        if not exists:
            raise serializers.ValidationError({"error": "No class with this section exists"})

        # Ensure student is part of this class and section
        if student_class != result_class or student_section != result_section:
            raise serializers.ValidationError({
                "error": f"Student {student.user.email} does not belong to class '{result_class.name}', section '{result_section.name}'"
            })

        return data

    def create(self, validated_data):
        return SubjectResult.objects.create(**validated_data)
