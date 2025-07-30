from rest_framework.views import APIView

from rest_framework import routers
from result.serializers import SubjectExamResultSerializer
from accounts.permissions import IsTeacher
from rest_framework.response import Response
class SubjectResultView(APIView):
    permission_classes = [IsTeacher]
    
    
    def get(self,request):
        pass
    def post(self,request):
        
        serialized_data = SubjectExamResultSerializer(data=request.data,many=True)
        if serialized_data.is_valid():
            serialized_data.save()
            print(serialized_data.data)
            return Response({"data":serialized_data.data})
        else:
            return Response({"Error":serialized_data.errors})
        
    
    

class ExamResultView(APIView):
    
    pass