
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
            'owner',
        ]
        read_only_fields = ["owner",]

class TaskDetailedSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner',]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'status',
            'deadline',
            'owner',
        )
        read_only_fields = ["owner",]

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("The deadline date can't be in the past.")
        return value