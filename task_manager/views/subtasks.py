from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from task_manager.serializers.subtasks import SubTaskSerializer, SubTaskCreateSerializer, SubTaskDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from task_manager.models import SubTask
from rest_framework.permissions import IsAuthenticatedOrReadOnly



class SubTaskListCreateAPIView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['status', 'deadline']

    search_fields = ['title', 'description']

    ordering_fields = ['created_at']
    ordering = ['created_at']


class SubTaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubTaskListCreateView(APIView, PageNumberPagination):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticatedOrReadOnly]
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
