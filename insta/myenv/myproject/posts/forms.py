
# forms.py
from django import forms
from .models import Video,Image,Article
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content', 'video','images','content_type']  # 필요한 필드들을 추가하거나 수정하세요
        
class LoginForm(AuthenticationForm):
    pass

# forms.py

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
