# queuetube/main_app/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Playlist, Video
from .forms import VideoForm, SearchForm
from django.http import Http404
from django.forms.utils import ErrorList
import requests
import urllib
import environ
env = environ.Env()

YOUTUBE_API_KEY = env('SECRET_KEY')

# Basic Views
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    return render(request, 'dashboard.html')


def add_video(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    playlist = Playlist.objects.get(pk=pk)
    if not playlist.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.playlist = playlist
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']                
                video.title = title
                video.save()
                return redirect('playlist_detail', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a Youtube URL')

    return render(request, 'video/add_video.html', {'form': form, 'search_form': search_form, 'playlist':playlist})

# Playlist Views
class PlaylistsIndex(generic.ListView):
    model = Playlist
    template_name = 'playlists/index.html'
    context_object_name = 'playlists'

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'
  
    def form_valid(self, form):
        super().form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.get_success_url())
      
# Oh CRUD

#Create
class CreatePlaylist(generic.CreateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/create_playlist.html'
    success_url = reverse_lazy('home')
  
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#Read
class DetailPlaylist(generic.DetailView):
    model = Playlist
    template_name = 'playlist/detail_playlist.html'

#Update
class UpdatePlaylist(generic.UpdateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/update_playlist.html'
    success_url = reverse_lazy('dashboard')

#Delete
class DeletePlaylist(generic.DeleteView):
    model = Playlist
    template_name = 'playlist/delete_playlist.html'
    success_url = reverse_lazy('dashboard')
