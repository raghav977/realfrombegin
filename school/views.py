from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from school.permissions import IsPrincipal
from .middleware import get_current_db_name
from .serializers import SchoolCreateSerializer
from django.contrib.auth import get_user_model
from accounts.models import Principal
from django.conf import settings
from django.db import connections, transaction
from django.db.utils import ProgrammingError
from django.core.management import call_command


User = get_user_model()


class CreateSchoolView(APIView):
    permission_classes = [IsAuthenticated]
    # required_permission = 'manage_school'

    def post(self, request):
        serializer = SchoolCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            school = serializer.save()
            create_db(school.school_code)  # your function to create DB/schema
            
            principal = request.user
            
            principal_data = {
                "username": principal.username,
                "email": principal.email,
                "first_name": principal.first_name,
                "last_name": principal.last_name,
                "is_active": principal.is_active,
                "is_staff": principal.is_staff,
                "is_superuser": principal.is_superuser,
                "password": principal.password,
                "role":principal.role
            }
            new_user = User.objects.using(school.school_code).create(**principal_data)
            # assign_role(new_user,'principal')
            principal = Principal.objects.using(school.school_code).create(user=new_user)
            return Response({"data": serializer.data}, status=201)
        return Response({"error": serializer.errors}, status=400)


def create_db(database_name):
    """
    Creates a new database and runs migrations on it.
    
    Args:
        database_name: Valid MySQL database name
    
    Raises:
        ValueError: For invalid database names
        ProgrammingError: For database errors
    """
    # if not is_valid_database_name(database_name):  # Implement this validation
        # raise ValueError("Invalid database name")

    try:
        # Use parameterized query if possible
        with connections['default'].cursor() as cursor:
            cursor.execute(f"CREATE DATABASE  `{database_name}`")
            transaction.commit()

        # Configure new database
        new_db_config = settings.DATABASES['default'].copy()
        new_db_config['NAME'] = database_name
        connections.databases[database_name] = new_db_config

        # Run migrations
        call_command('migrate', database=database_name)
        
    except ProgrammingError as e:
        print(f"Database creation failed: {e}")  # Use proper logging
        # Attempt to clean up if possible
        with connections['default'].cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS %s", [database_name])
        raise


class SchoolStatsView(APIView):
    permission_classes = [IsPrincipal]
    # required_permission = 'manage_school'

    def get(self, request):
        # Get current database (school) name
        db_name = get_current_db_name()

        if db_name == 'default':
            return Response({"error": "Not a school database"}, status=400)

        # Get counts from the current school database
        with connections[db_name].cursor() as cursor:
            # Count students
            cursor.execute("SELECT COUNT(*) FROM accounts_student")
            student_count = cursor.fetchone()[0]

            # Count teachers
            cursor.execute("SELECT COUNT(*) FROM accounts_teacher")
            teacher_count = cursor.fetchone()[0]

        return Response({
            "student_count": student_count,
            "teacher_count": teacher_count
        })