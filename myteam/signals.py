from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import TeamTasks, Feed


@receiver(m2m_changed, sender=TeamTasks.assinged_users.through)
def notify_assinged_users(sender, instance, action, pk_set, **kwargs):
    
    if action == 'post_add':
        for user_id in pk_set:
            Feed.objects.create(
                user_id = user_id,
                subject = 'New Team Task',
                content = f"You were assigned a new task: '{instance.topic}'"
            )

