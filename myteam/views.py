from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teams, TeamMessages

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