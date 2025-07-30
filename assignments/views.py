# assignment/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Assignment, AssignmentSubmission
from .serializers import (
    AssignmentSerializer,
    AssignmentPublishSerializer,
    AssignmentSubmissionSerializer,
    GradeSubmissionSerializer
)
from .permissions import IsTeacher, IsStudent
from django.shortcuts import get_object_or_404
from django.utils import timezone
# from django.db.models import Q


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        return Assignment.objects.filter(teacher_subject_section__teacher=teacher).order_by('-created_at')

    def perform_create(self, serializer):
        
        serializer.save()


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Assignment.objects.all()

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        return Assignment.objects.filter(teacher=teacher)


class PublishAssignmentView(generics.UpdateAPIView):
    serializer_class = AssignmentPublishSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = Assignment.objects.all()

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        return Assignment.objects.filter(teacher=teacher)

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment.is_published = serializer.validated_data['is_published']
        assignment.save()

        return Response({'status': 'success', 'is_published': assignment.is_published})


class StudentAssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        student = self.request.user.user_student
        student_classroom = student.section.class_room
        student_section = student.section.section
        

        return Assignment.objects.filter(
            
            teacher_subject_section__section=student_section,teacher_subject_section__class_subject__class_obj=student_classroom,
            is_published=True
        ).order_by('-due_date')


class AssignmentSubmissionCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        assignment = get_object_or_404(
            Assignment,
            id=self.kwargs['assignment_id'],
            is_published=True
        )
        student = self.request.user.user_student
        assignment_classroom = assignment.teacher_subject_section.class_subject.class_obj
        assignment_section = assignment.teacher_subject_section.section

        student_class_room = student.section.class_room
        student_section = student.section.section
        
        

        print("This is student class room",student_class_room)
        

        print("This is student section",student_section)
        

        
        print("This is assignment classroom",assignment_classroom)
        

        print("This is assignment section ", assignment_section)
        


        if assignment_classroom!=student_class_room and assignment_section!=student_section:
            print("Yo assignment tero lagi haina")
            return Response({"error":"Yo assignment tero lagi haina"})
        
        # Check if the student is in the correct section
        # if student.section != assignment.section:
        #     return Response(
        #         {'error': 'This assignment is not for your section.'},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        # Check if submission already exists
        if AssignmentSubmission.objects.filter(assignment=assignment, student=student).exists():
            return Response(
                {'error': 'You have already submitted this assignment.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(assignment=assignment, student=student)


class TeacherSubmissionListView(generics.ListAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        assignment = get_object_or_404(
            Assignment,
            id=self.kwargs['assignment_id'],
            teacher=teacher
        )
        return AssignmentSubmission.objects.filter(assignment=assignment)


class GradeSubmissionView(generics.UpdateAPIView):
    serializer_class = GradeSubmissionSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    queryset = AssignmentSubmission.objects.all()

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        return AssignmentSubmission.objects.filter(assignment__teacher_subject_section__teacher=teacher)

    def update(self, request, *args, **kwargs):
        submission = self.get_object()

        # Check if marks exceed assignment total marks
        marks_obtained = request.data.get('marks_obtained')
        if marks_obtained and int(marks_obtained) > submission.assignment.total_marks:
            return Response(
                {'error': 'Marks obtained cannot exceed assignment total marks.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)


class StudentSubmissionListView(generics.ListAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        student = self.request.user.user_student
        return AssignmentSubmission.objects.filter(student=student)