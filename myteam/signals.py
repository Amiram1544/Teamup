from django.db.models.signals import m2m_changed, post_save 
from django.dispatch import receiver
from .models import TeamTasks, Feed, TeamMessages, Directs
from django.utils import timezone


@receiver(m2m_changed, sender=TeamTasks.assinged_users.through)
def notify_assinged_users(sender, instance, action, pk_set, **kwargs):
    
    if action == 'post_add':
        for user_id in pk_set:
            Feed.objects.create(
                user_id = user_id,
                subject = 'New Team Task',
                content = f"You were assigned a new task: '{instance.topic}'"
            )

@receiver(post_save, sender=TeamMessages)
def new_message_notify(sender, instance, created, **kwargs):
    team = instance.team
    sender_user = instance.user
    
    for member in team.members.exclude(id=sender_user.id):
        if created:
            Feed.objects.create(
               user = member,
               subject = "New team message: ",
               content = f"{sender_user.username} in {instance.team} said {instance.body[:30]}",
               timestamp = timezone.now(),
               team=team,
            )
            
@receiver(post_save, sender=Directs)           
def unseen_message(sender, instance, created, **kwargs):
    
    if created:
        receiver = instance.receiver
        senderUser = instance.sender
        
        Feed.objects.create(
            user = receiver,
            subject = "New Direct Message",
            content = f"New message from {senderUser.username} : {instance.body[:30]}",
            sender_user = senderUser,
            timestamp = timezone.now(),
        )