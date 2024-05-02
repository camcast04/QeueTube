# queuetube/main_app/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    # one playlist can hold many videos 
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)