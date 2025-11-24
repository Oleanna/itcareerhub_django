
from rest_framework import serializers

from task_manager.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get("name")
        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        new_name = validated_data.get("name", instance.name)
        if Category.objects.exclude(pk=instance.pk).filter(name=new_name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        instance.name = new_name
        instance.save()
        return instance