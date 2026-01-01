from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.serializers.tasks import TaskDetailedSerializer
from django.db.models import Count, Q
from task_manager.enums import TaskStatus
from task_manager.models import Task, SubTask
from task_manager.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from task_manager.permissions.tasks import IsOwnerOrReadOnly


from paginators import OverrideCursorPaginator

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["status", "deadline"]

    search_fields = ["title", "description"]

    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskListSerializer

class MyTaskListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailedSerializer
    pagination_class = OverrideCursorPaginator
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]
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
@permission_classes([AllowAny])
def task_list(request: Request) -> Response:
    tasks = Task.objects.all()
    tasks_dto = TaskListSerializer(tasks, many=True)

    return Response(
        data=tasks_dto.data,
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
