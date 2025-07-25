from rest_framework import serializers
from .models import ClassRoom, Section,Class_section
import pdb

class SectionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id','name']
class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['name']


class SectionClassRoomSerializer(serializers.Serializer):
    # class_room = serializers.IntegerField()
    class_room = serializers.DictField()
    # section = serializers.ListField(child=serializers.CharField())
    # section = serializers.ListField(child=serializers.CharField())
    section = serializers.ListField(child=serializers.DictField())

    
    def validate(self,data):
        print("This is data",data)
        return data
class ClassSectionOutputSerializer(serializers.ModelSerializer):
    class_room = serializers.CharField(source='class_room.name')
    section = serializers.CharField(source='section.name')

    class Meta:
        model = Class_section
        fields = ['id', 'class_room', 'section']

    