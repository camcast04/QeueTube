# queuetube/main_app/views.py

import urllib.parse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Playlist, Video
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import urllib
import environ
env = environ.Env()

YOUTUBE_API_KEY = env('YOUTUBE_API_KEY')

# Basic Views
def home(request):
    popular_playlists = Playlist.objects.all().order_by('-id')[:3]
    return render(request, 'home.html', {'popular_playlists':popular_playlists})

def about(request):
    return render(request, 'about.html')


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

@login_required
def dashboard(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'playlists': playlists})


#video views
@login_required
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
                return redirect('detail_playlist', pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Needs to be a Youtube URL')

    return render(request, 'video/add_video.html', {'form': form, 'search_form': search_form, 'playlist':playlist})

#Add Video
@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        #grab this 
        return JsonResponse(response.json())
    return JsonResponse({
            'error':'broken -- form not validated'
        })

#Delete Video  
class DeleteVideo(generic.DeleteView):
    model = Video 
    template_name = 'video/delete_video.html'
    success_url = reverse_lazy('dashboard')





# Playlist Views     
# Oh CRUD

#Create
class CreatePlaylist(LoginRequiredMixin, generic.CreateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/create_playlist.html'
    success_url = reverse_lazy('dashboard')
  
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreatePlaylist, self).form_valid(form)
        return redirect('dashboard')
    

#Read
class DetailPlaylist(generic.DetailView):
    model = Playlist
    template_name = 'playlist/detail_playlist.html'

#Update
class UpdatePlaylist(LoginRequiredMixin, generic.UpdateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/update_playlist.html'
    success_url = reverse_lazy('dashboard')

#Delete
class DeletePlaylist(LoginRequiredMixin, generic.DeleteView):
    model = Playlist
    template_name = 'playlist/delete_playlist.html'
    success_url = reverse_lazy('dashboard')
    

#View all ... views

@login_required
def all_playlists(request):
    playlists = Playlist.objects.all().order_by('-id')
    return render(request, 'playlist/all_playlists.html', {'playlists': playlists})


@login_required
def user_playlists(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    playlists = Playlist.objects.filter(user=user).order_by('-id')
    return render(request, 'playlist/user_playlists.html', {'playlists': playlists, 'playlist_user': user})

