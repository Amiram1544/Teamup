from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomAuth(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        try:
            user = UserModel.objects.get(email = username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username = username)
            except UserModel.DoesNotExist:
                return None
            
        if user.check_password(password):
            return user
        return None