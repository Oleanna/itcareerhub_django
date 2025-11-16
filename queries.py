import os
from datetime import date, timezone, timedelta
from task_manager.enums import TaskStatus
from django.utils import timezone

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from task_manager.models import Task, SubTask, Category

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status=TaskStatus.new,
    deadline=timezone.now() + timedelta(days=3)
)

subTask = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status=TaskStatus.new,
    deadline=timezone.now() + timedelta(days=2),
    task=task
)

subTask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status=TaskStatus.new,
    deadline=timezone.now() + timedelta(days=1),
    task=task
)


new_tasks = Task.objects.filter(status=TaskStatus.new)


overdue_subtasks = SubTask.objects.filter(
    status=TaskStatus.done,
    deadline__lt=timezone.now()
)


Task.objects.filter(title="Prepare presentation").delete()


