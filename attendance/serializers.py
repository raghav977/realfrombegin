from rest_framework import serializers
from attendance.models import Attendance, StudentAttendance
from section.models import ClassTeacher
from accounts.models import Student


class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['student', 'status', 'remarks']


class CreateAttendanceSerializer(serializers.ModelSerializer):
    student_attendances = StudentAttendanceSerializer(many=True)

    class Meta:
        model = Attendance
        fields = ['class_teacher', 'date', 'student_attendances']

    def validate(self, data):
        class_teacher = data.get('class_teacher')
        students_data = data.get('student_attendances', [])
        print("This is clss teacher",class_teacher)

        # Get the section from the class teacher
        section = class_teacher.section

        for student_data in students_data:
            student = student_data.get('student')
            if student.section != section:
                raise serializers.ValidationError(
                    f"Student-with id -{student.id} {student.user.email} does not belong to {section.class_room.name} section {section.section.name}."
                )

        return data

    def create(self, validated_data):
        student_attendance_data = validated_data.pop('student_attendances')
        attendance = Attendance.objects.create(**validated_data)

        for entry in student_attendance_data:
            StudentAttendance.objects.create(attendance=attendance, **entry)

        return attendance
