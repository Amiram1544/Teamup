from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Rooms
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def room(request,pk):
    
    rooms = Rooms.objects.get(id=pk)
    participants = rooms.participants.all()
    
    if not room:
        messages.warning(request, 'Room not found')
        return redirect('home')
    
    
    context = {
        'rooms': rooms,
        'participants' : participants,
    }
    return render(request, 'chatrooms/room.html', context)