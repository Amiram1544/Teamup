from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teams, TeamMessages
from django.contrib import messages

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