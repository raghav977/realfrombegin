from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
# Create your views here.
from .models import ClassRoom,Section
# from .serializers import SectionSerializer
# from school.permissions import
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from .models import ClassRoom,Class_section
from .serializers import SectionClassRoomSerializer,ClassSectionOutputSerializer
# from school.permissions import HasSchoolPermission
from rest_framework.response import Response
from rest_framework.views import APIView


class IsPrincipal:
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'principal'
    pass
class CreateClassWithSectionsView(APIView):
    permission_classes = [IsPrincipal]

    def get(self,request):
        class_section = Class_section.objects.all()
        serializer = ClassSectionOutputSerializer(class_section,many=True)
        return Response({"data":serializer.data})
    def post(self, request):
        data = request.data
        print("Incoming data:", data)

        serializer = SectionClassRoomSerializer(data=data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=400)

        all_class_sections = []

        for item in serializer.validated_data:
            print("This is serializer.validated_data",serializer.validated_data)
            data = serializer.validated_data
            # import pdb; pdb.set_trace() # Execution will pause here
            print("This is item",item)
            item =str(item)
            # import pdb; pdb.set_trace() # Execution will pause here


            class_room_data = data["class_room"]
            section_list = data["section"]

            class_room, _ = ClassRoom.objects.get_or_create(
                name=class_room_data["name"],
                defaults=class_room_data
            )

            for sec in section_list:
                section_obj, _ = Section.objects.get_or_create(name=sec["name"])
                class_section, _ = Class_section.objects.get_or_create(
                    class_room=class_room,
                    section=section_obj
                )
                all_class_sections.append(class_section)

        output_serializer = ClassSectionOutputSerializer(all_class_sections, many=True)
        return Response({"data": output_serializer.data})
