
from rest_framework import serializers
from django.utils import timezone
from task_manager.models import Task
from task_manager.serializers.subtasks import SubTaskSerializer


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'deadline',
        ]

class TaskDetailedSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'deadline',
        )

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("The deadline date can't be in the past.")
        return value