from django.utils import timezone
from django.db import models
from django.conf import settings
from task_manager.enums import TaskStatus


class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField('Category', related_name='tasks', blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices(),default=TaskStatus.new)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


