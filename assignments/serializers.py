# assignment/serializers.py
from rest_framework import serializers
from .models import Assignment, AssignmentSubmission
from subjects.models import Subject,SectionSubjectTeacher
from classes.models import Section


class AssignmentSerializer(serializers.ModelSerializer):
    # teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    # subject_name = serializers.CharField(source='subject.name', read_only=True)
    # section_name = serializers.CharField(source='section.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher_subject_section.teacher.user.email',read_only=True)
    section_name = serializers.CharField(source='teacher_subject_section.section.name',read_only=True)
    class_name = serializers.CharField(source='teacher_subject_section.class_subject.class_obj.name',read_only=True)
    subject_name = serializers.CharField(source='teacher_subject_section.class_subject.subject.subject_name',read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 'due_date', 'created_at', 'updated_at','class_name', 'teacher_name', 'subject_name', 'teacher_subject_section',
            'section_name', 'total_marks', 'is_published'
        ]
        read_only_fields = ['teacher']

    def validate(self, data):
        # Ensure the teacher is assigned to the section
        teacher = self.context['request'].user.user_teacher
        
        print("This is teacher",teacher)
        print("This is data",data)
        
        teacher_section_subject_id = data.get('teacher_subject_section')
        
        
        # teacher section subject id ma teacher le padaune section subject hunxa
        
        # aba check garne ki tyo teacher chai actually belong garxa ki gardaina? hamro section ma ra usle kei padauxa ki padaudaina
        
        teacher_exist_in_that_section = SectionSubjectTeacher.objects.get(teacher=teacher)
        
        if teacher_exist_in_that_section is None:
            print("You are not assigned to any subjects and to any sections")
            raise serializers.ValidationError({"error":"You are not assigned to any subjects and to any sections"})
        print("Okay you are assigned to teach ")
        import pdb; pdb.set_trace()

        if teacher_exist_in_that_section.teacher != teacher:
            print("You are not the teacher to give assignment for this subject")
            raise serializers.ValidationError({"error":"You are not the teacher to give assignment for this subject"})
        import pdb; pdb.set_trace()

        print("You are the teacher you can give the assignment")
        
        import pdb; pdb.set_trace()

        # print("T")
        # is_that_teacher_exist_in_that_section = teacher_subject_section.objects.filter(teacher__user = )
        return data
        # if 'section' in data and data['section'] not in teacher.sections.all():
        #     raise serializers.ValidationError("You are not assigned to this section.")

        # # Ensure the teacher teaches the subject
        # if 'subject' in data and data['subject'] not in teacher.subject.all():
        #     raise serializers.ValidationError("You don't teach this subject.")

        # return data


class AssignmentPublishSerializer(serializers.Serializer):
    is_published = serializers.BooleanField()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'assignment_title', 'student', 'student_name',
            'submission_date', 'submission_file', 'remarks', 'marks_obtained', 'is_graded'
        ]
        read_only_fields = ['student', 'submission_date']


class GradeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['remarks', 'marks_obtained', 'is_graded']