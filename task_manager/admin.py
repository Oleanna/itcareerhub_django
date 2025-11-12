
from django.contrib import admin
from task_manager.models import Category, SubTask, Task

admin.site.register(Task)
admin.site.register(Category)
admin.site.register(SubTask)


