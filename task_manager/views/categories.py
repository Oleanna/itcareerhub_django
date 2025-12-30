from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from task_manager.models import Category
from task_manager.serializers import CategoryCreateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=False, url_path='tasks/count', permission_classes = [IsAuthenticatedOrReadOnly])
    def get_tasks_count(self, request):
        count_tasks = (
            Category.objects
            .values('name')
            .annotate(cnt_tasks=Count('tasks'))
        )

        return Response(
            data=count_tasks,
            status=status.HTTP_200_OK
        )