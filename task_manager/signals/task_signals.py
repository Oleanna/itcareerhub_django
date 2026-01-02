from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from task_manager.models import Task
from task_manager.enums import TaskStatus


@receiver(pre_save, sender=Task)
def store_old_task_status(sender, instance: Task, **kwargs):

    if not instance.pk:
        instance._old_status = None
        return

    try:
        old_task = Task.objects.get(pk=instance.pk)
        instance._old_status = old_task.status
    except Task.DoesNotExist:
        instance._old_status = None

@receiver(post_save, sender=Task)
def notify_owner_on_status_change(
    sender,
    instance: Task,
    created: bool,
    **kwargs,
):
    if created:
        return

    old_status = getattr(instance, "_old_status", None)
    new_status = instance.status

    if old_status is None:
        return
    if old_status == new_status:
        return

    message = (
        f"Hello {instance.owner.username},\n\n"
        f"Your task \"{instance.title}\" status has been updated.\n\n"
        f"Previous status: {old_status}\n"
        f"Current status: {new_status}\n"
    )

    send_mail(
        subject="Task status updated",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.owner.email],
        fail_silently=True,
    )
