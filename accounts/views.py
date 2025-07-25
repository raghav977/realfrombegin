from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, get_user_model, authenticate
from rolepermissions.roles import assign_role
from django.http import HttpResponse
from rest_framework import status
from accounts.permissions import IsPrincipal, IsStaffOrPrincipal, IsSchoolStaff, IsTeacher, IsStudent

import google.oauth2.id_token
import google.auth.transport.requests
from datetime import datetime, timezone
import os
from django.shortcuts import redirect
from school.models import School
from accounts.models import Principal,TeacherSection
from accounts.serializers import TeacherCreateSerializer, TeacherSectionSerializer,StaffCreateSerializer, TeacherProfileSerializer,StudentCreateSerializer,TeacherReadSerializer, PrincipalProfileSerializer, StaffProfileSerializer
from accounts.permissions import IsPrincipal, IsStaffOrPrincipal, IsTeacher, IsStudent

User = get_user_model()

from decouple import config

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')






def create_principal(user):
    principal = Principal.objects.create(user=user)
    print("This is principal",principal)
    return principal
def verify_google_token_with_skew(id_token_str, audience, clock_skew=10):
    try:
        request_adapter = google.auth.transport.requests.Request()
        idinfo = google.oauth2.id_token.verify_oauth2_token(
            id_token_str, request_adapter, audience=audience
        )

        now = datetime.now(timezone.utc).timestamp()

        if idinfo.get('nbf') and now + clock_skew < idinfo['nbf']:
            raise ValueError("Token not yet valid")

        if idinfo.get('exp') and now - clock_skew > idinfo['exp']:
            raise ValueError("Token expired")

        return idinfo

    except Exception as e:
        print("❌ Token verification failed:", e)
        raise


class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        id_token_str = request.data.get('id_token')
        if not id_token_str:
            return Response({'error': 'No token provided'}, status=400)

        try:
            idinfo = verify_google_token_with_skew(id_token_str, GOOGLE_CLIENT_ID)
            email = idinfo.get('email')
            name = idinfo.get('name')

            # Create user if not exist
            user, created = User.objects.get_or_create(email=email,username=email,defaults={"first_name": name})
            
            
            # assign_role(user, 'principal')
            if created:
                # print(assign_role(user, 'principal'))
                user.role = 'principal'  
                principal=create_principal(user)
                print("This is principal",principal)
                user.set_unusable_password()  
                user.save()
                # assign_role(user, 'principal')
                # print(assign_role(user, 'principal'))
                print(f"🆕 Created new principal: {email}")
            else:
                print(f"✅ Logging in existing user: {email}")
                school=School.objects.filter(created_by=user).first()
                print("school exist")
                refresh = RefreshToken.for_user(user)
                
               
                
                if not school:
                    
                    print("This is access token",str(refresh.access_token))
                    print("\nThis is refresh token",str(refresh))
                    
                    return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'first_name': user.first_name,
                'email': user.email,
            })
                    
                school_code = school.school_code
                
                refresh = RefreshToken.for_user(user)
                
                print("\nThis is refresh token",str(refresh))
                print("This is access token",str(refresh.access_token))
                
                return Response({'access': str(refresh.access_token),
                'refresh': str(refresh),
                'first_name': user.first_name,
                'email': user.email,"redirect_url": f"http://{school_code}.localhost:5173/dashboard/"})

                
                    
                

            
            request.session.flush()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'first_name': user.first_name,
                'email': user.email,
            })

        except Exception as e:
            print("❌ Login error:", e)
            return Response({'error': 'Invalid token', 'details': str(e)}, status=400)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh'))
        refresh_token.blacklist()
        return Response({
            "Token": "Token Expired"
        }, status=200)

class StudentCreation:
    pass

class CreateStaffView(APIView):
    print("Etaaa????????")
    # permission_classes = [IsAuthenticated]
    
    
    permission_classes = [IsPrincipal]

    def post(self, request):
        serializer = StaffCreateSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response({
                'message': 'Staff account created successfully',
                'staff_id': staff.id,
                'email': staff.user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from accounts.models import Teacher
class CreateTeacherView(APIView):
    permission_classes = [IsStaffOrPrincipal]
    
    def get(self,request):
        dt = Teacher.objects.all()
        serial = serial = TeacherReadSerializer(dt, many=True)

        return Response({"teachers":serial.data},status=200)
        # return Response({"Errors":serial.errors},status=400)

    def post(self, request):
        serializer = TeacherCreateSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            print("This is teacher saved",teacher)
            return Response({
                'message': 'Teacher account created successfully',
                'teacher_id': teacher.id,
                'email': teacher.user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from classes.models import Section
class TeacherSection(APIView):
    permission_classes=[IsPrincipal]
    
    def post(self,request):
        teacher = TeacherSectionSerializer(data=request.data)
        if teacher.is_valid():
            teacher.save()
            return Response({"data":teacher.data},status=200)
        
        else:
            return Response({"error":teacher.errors},status=400)
        
class CreateStudentView(APIView):
    permission_classes = [IsStaffOrPrincipal]

    def post(self, request):
        # print(Section.objects.filter(id=2))
        print("The data are",request.data)
        serializer = StudentCreateSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'message': 'Student account created successfully',
                'student_id': student.id,
                'email': student.user.email,
                'section':student.section.section.name,
                'class':student.section.class_room.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrincipalProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsPrincipal]
    serializer_class = PrincipalProfileSerializer

    def get_object(self):
        return Principal.objects.get(user=self.request.user)


class PrincipalDeleteView(DestroyAPIView):
    permission_classes = [IsPrincipal]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Delete associated school if exists
        if hasattr(instance, 'principal_profile') and instance.principal_profile.school:
            instance.principal_profile.school.delete()

        # Logout by blacklisting token
        from rest_framework_simplejwt.tokens import RefreshToken
        RefreshToken.for_user(instance).blacklist()

        instance.delete()
        return Response(
            {"message": "Principal account and associated data deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )



class StaffProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsSchoolStaff]
    serializer_class = StaffProfileSerializer

    def get_object(self):
        return self.request.user.user_staff


class StaffDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Logout by blacklisting token
        from rest_framework_simplejwt.tokens import RefreshToken
        RefreshToken.for_user(instance).blacklist()

        instance.delete()
        return Response(
            {"message": "Staff account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class StaffLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        if user.role != 'staff':
            return Response({'error': 'Not a staff account'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'first_name': user.first_name,
            'email': user.email,
            'role': user.role
        })



class TeacherLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)
        print("This is email",email)
        print("This is password",password)
        user = User.objects.get(email=email)
        
        # print("User exits",user)
        # print(user.check_password(password))
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        if user.role != 'teacher':
            return Response({'error': 'Not a teacher account'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'first_name': user.first_name,
            'email': user.email,
            'role': user.role
        })

class TeacherProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = TeacherProfileSerializer

    def get_object(self):
        return self.request.user.user_teacher

class TeacherDeleteView(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsTeacher]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Logout by blacklisting token
        refresh = RefreshToken.for_user(instance)
        refresh.blacklist()

        instance.delete()
        return Response(
            {"message": "Teacher account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class StudentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        if user.role != 'student':
            return Response({'error': 'Not a student account'}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'first_name': user.first_name,
            'email': user.email,
            'role': user.role,
            'student_id': user.user_student.id
        })

class StudentProfileView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated, IsStudent]
    # serializer_class = StudentProfileSerializer

    def get_object(self):
        return self.request.user.user_student

class StudentDeleteView(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsStudent]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # Logout by blacklisting token
        refresh = RefreshToken.for_user(instance)
        refresh.blacklist()

        instance.delete()
        return Response(
            {"message": "Student account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )