from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from task_manager.enums import TaskStatus


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField('Category', related_name='tasks', blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices(),default=TaskStatus.new)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
