from rest_framework import viewsets, status
from rest_framework.response import Response
from attendance.models import Attendance
from attendance.serializers import CreateAttendanceSerializer
from rest_framework.permissions import IsAuthenticated


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = CreateAttendanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        print("This is validated data",serializer.validated_data)
        # Optional: Prevent duplicate attendance for same class/date
        class_teacher = serializer.validated_data['class_teacher']
        print("This is class teacher",class_teacher)
        
        # date = serializer.validated_data['date']
        import datetime
        today = datetime.date.today()

        if Attendance.objects.filter(class_teacher=class_teacher, date=today).exists():
            return Response(
                {"detail": f"Attendance already exists for {class_teacher} on {today}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
