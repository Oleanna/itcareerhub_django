from django.db import models
from django.utils import timezone
from task_manager.models.managers import SoftDeleteManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    all_objects = models.Manager()
    objects = SoftDeleteManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()



