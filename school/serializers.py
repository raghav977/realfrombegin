# serializers.py
from rest_framework import serializers
from .models import School,AcademicYear
class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['academic_year']

class SchoolCreateSerializer(serializers.ModelSerializer):
    academic_year = AcademicSerializer()

    class Meta:
        model = School
        fields = ['school_name', 'school_code', 'established_date', 'pan_no', 'academic_year']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        # Step 1: Extract academic year data
        academic_data = validated_data.pop('academic_year')
        print("This is academic_data",academic_data)
        # Step 2: Create AcademicYear FIRST
        academic_instance = AcademicYear.objects.create(**academic_data)
        
        # Step 3: Then create School with academic_year FK
        school = School.objects.create(academic_year=academic_instance,created_by=user, **validated_data)
        # print("The user is ")
        
        return school
