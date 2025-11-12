from django.utils import timezone

from django.db import models

from task_manager.enums import TaskStatus


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    task = models.ForeignKey('Task', related_name='subtask', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=TaskStatus.choices(), default=TaskStatus.new)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title