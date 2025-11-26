from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Count, Q

from task_manager.enums import TaskStatus
from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskListSerializer,
    TaskCreateSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from task_manager.serializers.subtasks import SubTaskSerializer, SubTaskCreateSerializer

WEEKDAYS = {
    "sunday": 1,
    "monday": 2,
    "tuesday": 3,
    "wednesday": 4,
    "thursday": 5,
    "friday": 6,
    "saturday": 7,
}

class TaskByWeekday(APIView):
    def get(self, request: Request):
        weekday = request.query_params.get("weekday")
        queryset = Task.objects.all()
        if not weekday:
            task_dto =TaskListSerializer(queryset, many=True)
            return Response(task_dto.data, status=status.HTTP_200_OK)

        weekday_param = weekday.lower()

        if weekday_param not in WEEKDAYS:
            return Response({"error": "Invalid weekday"}, status=status.HTTP_400_BAD_REQUEST)

        target_weekday = WEEKDAYS[weekday_param]
        queryset = queryset.filter(deadline__week_day=target_weekday)

        task_dto = TaskListSerializer(queryset, many=True)
        return Response(task_dto.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def task_list(request: Request) -> Response:
    tasks = Task.objects.all()
    tasks_dto = TaskListSerializer(tasks, many=True)

    return Response(
        data=tasks_dto.data,
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def task_create(request: Request) -> Response:
    task_dto = TaskCreateSerializer(data=request.data)

    if not task_dto.is_valid():
        return Response(
            data=task_dto.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        task_dto.save()
    except Exception as exc:
        return Response(
            data={
                "error": f"Error when creating a task: ",
                "detail": f"{str(exc)}"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        data=task_dto.data,
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def task_detail(request: Request, task_id: int) -> Response:
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response(
            data={"error": f"Task with id={task_id} not found"},
                  status=status.HTTP_404_NOT_FOUND
        )
    task_dto = TaskListSerializer(task)

    return Response(
        data=task_dto.data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def task_status(request: Request):
    try:
        total_tasks = Task.objects.count()

        tasks_by_status_qs = (
            Task.objects
            .values('status')
            .annotate(count=Count('id'))
        )
        tasks_by_status = [{"status": value['status'], "count": value['count']} for value in tasks_by_status_qs]

        overdue_tasks = Task.objects.filter(
            ~Q(status=TaskStatus.done),
            deadline__lte=timezone.now().date()
        ).count()

        return Response(
            data={
            "total_tasks": total_tasks,
            "tasks_by_status": tasks_by_status,
            "overdue_tasks": overdue_tasks,
        },
            status=status.HTTP_200_OK
        )

    except Exception as exc:
        return Response(
            data={"error": f"Error while getting task statistics: {str(exc)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5
    def get(self, request):
        queryset = SubTask.objects.all().order_by("-created_at")

        task_name = request.query_params.get("task_name")
        status_param = request.query_params.get("status")

        if task_name:
            queryset = queryset.filter(task__title__icontains=task_name)

        if status_param:
            queryset = queryset.filter(status=status_param)

        paginated_subtasks = self.paginate_queryset(queryset, request, view=self)
        serializer = SubTaskSerializer(paginated_subtasks, many=True)

        return self.get_paginated_response(serializer.data)


    def post(self, request):
        subtasks_dto = SubTaskCreateSerializer(data=request.data)
        if subtasks_dto.is_valid():
            subtask = subtasks_dto.save()
            return Response(SubTaskSerializer(subtask).data, status=status.HTTP_201_CREATED)
        return Response(subtasks_dto.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, subtask_id):
        try:
            return SubTask.objects.get(pk=subtask_id)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, subtask_id):
        obj = self.get_object(subtask_id)
        if not obj:
            return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)
        subtask_dto = SubTaskSerializer(obj)
        return Response(subtask_dto.data, status=status.HTTP_200_OK)

    def put(self, request, subtask_id):
        obj = self.get_object(subtask_id)
        if not obj:
            return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)
        subtask_dto = SubTaskCreateSerializer(obj, data=request.data)
        if subtask_dto.is_valid():
            subtask_dto.save()
            return Response(subtask_dto.data, status=status.HTTP_200_OK)
        return Response(subtask_dto.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subtask_id):
        obj = self.get_object(subtask_id)
        if not obj:
            return Response({"error": "Subtask not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
