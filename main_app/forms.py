from .models import Video
from django import forms

class VideoForm(forms.ModelForm):
    model = Video 
    fields = ['title', 'url', 'youtube_id']