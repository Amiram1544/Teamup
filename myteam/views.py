from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teams, TeamMessages, ToDo
from django.contrib import messages
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt #only for development
import json


# Create your views here.

@login_required(login_url='login')
def mainpage(request):
    
    teams = Teams.objects.filter(members = request.user)
    for team in teams:
        team.first_members = team.members.all()[0:3]
        team.other_members_count = team.members.count() - 3
           
    context = {
        'teams': teams,
    }
    return render(request, 'myteam/mainpage.html', context)

@login_required(login_url='login')
def team_chat(request, team_id):
    
    team_page = Teams.objects.get(id=team_id)
    team_members = team_page.members.all()
    team_messages = TeamMessages.objects.filter(team=team_page).order_by('created')
    parent_id = request.POST.get('parent_id')
    
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
        
        return JsonResponse({
            'success' : True,
            'task' : {
                'id' : task.id,
                'topic': task.topic,
                'description' : task.description,
                'notes' : task.notes,   
            }
        })
        
    return JsonResponse ({'success': False}, status=400)