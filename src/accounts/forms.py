#from allauth.socialaccount.forms import SignupForm as SocialSignupForm
#from allauth.account.forms import SignupForm 
#from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from .models import Profile
from extra_views import InlineFormSetFactory
User = get_user_model()
from .models import Profile

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")
        labels = {"username": "Display name",}


class ProfileInline(InlineFormSetFactory):
    model = Profile
    fields = ['mobile_number']
    factory_kwargs={'can_delete': False}













    
    