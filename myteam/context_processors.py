from .models import Feed


def unseen_feed(request):
    
    if request.user.is_authenticated:
        
        unseen_count = request.user.activities.filter(user=request.user, seen=False).count()
        
        return {
            'unseen_count': unseen_count
        }
        
    return {}