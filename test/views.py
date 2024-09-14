from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from celery.result import AsyncResult

from .tasks import my_task,delete_old_locations
from .serializers import TipWriteSerializer
        
class Check(APIView):
    def post(self, request):
        try:            
            result = my_task.delay(3,5)

            if result.ready():
                task_result = result.get()  # This will get the result if it's done
                print(task_result, 'Task result')
                return Response({"message": "Task completed", "result": task_result})
            else:
                return Response({"message": "Task is still running", "task_id": result.id})
        
        except Exception as e:
            return Response({"error": str(e)})
        

class TaskStatus(APIView):
    def get(self, request, task_id):
        try:
            result = AsyncResult(task_id)

            if result.ready():
                task_result = result.get()  # Retrieve the result if task is done
                return Response({"message": "Task completed", "result": task_result})
            else:
                return Response({"message": "Task is still running"})
        
        except Exception as e:
            return Response({"error": str(e)})
        

class CreateTip(APIView):
    @swagger_auto_schema(
    operation_description="Create Tip",
    operation_id="tip create",
    request_body=TipWriteSerializer
    )
    def post(self,request):
        try:
            serializer = TipWriteSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"error":serializer.errors})
            serializer.save()
            return Response({"message":"tip created"})
        except Exception as e:
            return Response({"error":e})
        
class DeleteTip(APIView):
    @swagger_auto_schema(
    operation_description="Delete Tip",
    operation_id="tip delete"
    )
    def post(self,request):
        try:
            print("started")
            result = delete_old_locations.delay()
            if result.ready():
                    task_result = result.get()  # This will get the result if it's done
                    print(task_result, 'Task result')
                    return Response({"message": "Task completed", "result": task_result})
            else:
                return Response({"message": "Task is still running", "task_id": result.id})

        except Exception as e:
            return Response({"error":e})
        
        