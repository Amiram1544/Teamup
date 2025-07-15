from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teams, TeamMessages, ToDo, TeamTasks, Feed, Directs
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt #only for development
from django.views.decorators.http import require_POST
import json
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.

@login_required(login_url='login')
def mainpage(request):
    
    teams = Teams.objects.filter(members = request.user)
    
    unseen_count = Feed.objects.filter(user=request.user, seen=False).count()
    if unseen_count < 0:
        unseen_count = None
    
    for team in teams:
        team.first_members = team.members.all()[0:3]
        team.other_members_count = team.members.count() - 3
           
    context = {
        'teams': teams,
        'unseen_count': unseen_count,
    }
    return render(request, 'myteam/mainpage.html', context)

@login_required(login_url='login')
def team_chat(request, team_id):
    
    
    
    team_page = Teams.objects.get(id=team_id)
    team_members = team_page.members.all()
    team_messages = TeamMessages.objects.filter(team=team_page).order_by('created')
    parent_id = request.POST.get('parent_id')
    team_tasks = TeamTasks.objects.filter(team=team_page)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            team_message = request.POST.get('team_messages', '').strip()
            parent_message = None
            if parent_id:
                try:
                    parent_message = TeamMessages.objects.get(id=parent_id)
                except TeamMessages.DoesNotExist:
                    parent_message = None
                    
            if team_message:
                
                TeamMessages.objects.create( 
                    user = request.user,
                    team = team_page,
                    body = team_message,
                    parent = parent_message,  
                )
                messages.success(request, 'Sent')
                return redirect('myteam:team_chat', team_id=team_id)
            else:
                messages.error(request, 'Message cannot be empty. or an error occurred.')
            
            
    context = {
        'team_page': team_page,
        'team_messages': team_messages,
        'team_members': team_members,
        'team_tasks': team_tasks,
    }
    return render(request, 'myteam/team_chat.html', context)

@login_required(login_url='login')
def taskspage(request):
    
    tasks = ToDo.objects.filter(user=request.user).order_by('-created')
    today = now().date()
    

    context = {
        'tasks': tasks,
        'today': today,
    }
    return render(request, 'myteam/taskspage.html', context)

@csrf_exempt #development only, not for deployment
def add_task_ajax(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        topic = data.get('topic')
        description = data.get('description')
        notes = data.get('notes')
        
        task = ToDo.objects.create(
            user = request.user,
            topic = topic,
            description = description,
            notes = notes,
        )
        
        task.assinged_users.add(request.user)
        
        for user in task.assinged_users.all():
            Feed.objects.create(
                user = user,
                subject = topic,
                content = f"new task assigned {task.topic}"
            )
        
        return JsonResponse({
            'success' : True,
            'task' : {
                'id' : task.id,
                'topic': task.topic,
                'description' : task.description,
                'notes' : task.notes,
                'completed': task.completed,   
            }
        })
        
    return JsonResponse ({'success': False}, status=400)

@csrf_exempt #for development only
@require_POST
def complete_task_ajax(request):
    data = json.loads(request.body)
    task_id = data.get('id')
    
    try:
        
        task = ToDo.objects.get(id=task_id, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    
    except ToDo.DoesNotExist:
        
        return JsonResponse({'success': False}, status=400)
    
    
@csrf_exempt
@require_POST
def delete_task_ajax(request):
    data = json.loads(request.body)
    task_id = data.get('id')
    
    
    try:
        task = ToDo.objects.get(id = task_id, user = request.user)
        task.delete()
        return JsonResponse({'success': True})
    except ToDo.DoesNotExist:
        return JsonResponse({'success': False}, status = 404)
     
    
def news(request):
    
    feeds = request.user.activities.all()[:20]
    
    request.user.activities.filter(seen=False).update(seen=True)
    
    context ={
        'feeds' : feeds,
    }
    return render(request, 'myteam/news.html', context)


def team_task(request, team_id):
    
    team = get_object_or_404(Teams, id= team_id)
    tasks = TeamTasks.objects.filter(team=team)
    
    
    context = {
        'tasks': tasks,
    }
    return render(request, "myteam/team_task.html", context)

def get_user_tasks(request):
    
    user = request.user
    tasks = TeamTasks.objects.filter(assinged_users=user)
    
    context = {
        'tasks': tasks,
    }
    return render(request, 'myteam/get_user_tasks.html', context)

def get_conversation(user):
    
    texts = Directs.objects.filter(Q(sender=user) | Q(receiver= user))
    users = set()
    
    for text in texts:
        users.add(text.sender if text.sender!= user else text.receiver )
    return list(users)

def pv(request, username=None):
    
    users = get_conversation(request.user)
    target_user = None
    directs = []
    
    if username:
        target_user = get_object_or_404(User, username=username)
        
        directs = Directs.objects.filter(
            Q(sender=request.user , receiver=target_user) |
            Q(sender=target_user , receiver=request.user)
            ).order_by("timesent")
    
    context = {
        'directs': directs,
        'users': users,
        'target_user': target_user,
    }
    return render(request, 'myteam/pv.html', context)

@login_required(login_url='login')
def get_unseen(request):

    if request.user.is_authenticated:
        unseen_count = request.user.activities.filter(user=request.user, seen=False).count()
        
        return JsonResponse({'unseen_count': unseen_count})