
from rest_framework import serializers

from task_manager.models import SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = "__all__"
        read_only_fields = ("owner",)

class SubTaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = (
            "title",
            "description",
            "status",
            "deadline",
            "task",
            "owner",
        )
        read_only_fields = ("owner",)


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = (
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "task",
            "owner",
        )
        read_only_fields = ("owner",)


