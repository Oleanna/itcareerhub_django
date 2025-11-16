
from django.contrib import admin

from task_manager.enums import TaskStatus
from task_manager.models import Category, SubTask, Task

#admin.site.register(Task)
admin.site.register(Category)
#admin.site.register(SubTask)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'status',
        'task',
        'deadline',
        'created_at',
    ]
    actions = ['mark_as_done']

    @admin.action(description='Mark status as Done')
    def mark_as_done(self, request, queryset):
        queryset.update(status=TaskStatus.done)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = [
        'title',
        'description',
        'status',
        'deadline'
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    fields = [
        'title',
        'description',
        'status',
        'deadline',
        'created_at',
    ]
    list_display = [
        'title_short',
        'description',
        'status',
        'deadline',
        'created_at',

    ]

    @admin.display(description='title')
    def title_short(self, obj: Task):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title


