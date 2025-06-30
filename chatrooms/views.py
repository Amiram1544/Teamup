from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Rooms
from chatrooms.models import Messages
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def room(request,pk):
    
    rooms = Rooms.objects.get(id=pk)
    participants = rooms.participants.all()
    comments = Messages.objects.filter(rooms=rooms).order_by('created')
    parent_id = request.POST.get('parent_id')
    
    if not room:
        messages.warning(request, 'Room not found')
        return redirect('home')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = request.POST.get('comment', '').strip()
            parent_message = None
            if parent_id:
                try:
                    parent_message= Messages.objects.get(id=parent_id)
                except Messages.DoesNotExist:
                    parent_message = None
                                    
            if comment:
                
                Messages.objects.create(
                    user = request.user,
                    rooms = rooms,
                    body = comment,
                    parent = parent_message
                )
                rooms.participants.add(request.user)
                messages.success(request, 'Message sent succesfully.')
                return redirect('chatrooms:room', pk=pk)
            else:
                messages.error(request, 'Message cannot be empty.')
            
    
    context = {
        'rooms': rooms,
        'participants' : participants,
        'comments': comments,
        
    }
    return render(request, 'chatrooms/room.html', context)