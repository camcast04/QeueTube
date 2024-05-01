from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Playlist, Video
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
# Create your views here.
def home(request):
  return render(request, 'home.html')


def dashboard(request):
  return render(request, 'dashboard.html')

def about(request):
  return render(request, 'about.html')

def playlists_index(request): #all views functions have to accept a request object
  playlist = Playlist.objects.all()
  return render(request, 'playlists/index.html', { #not only going render a template but also gather data
    'playlists': playlists #this third argument: we need to pass a context dictionary -> list of playlist dictionaries
    #remember in the database it will be saved as a dictionary/database (playlists) with several entries like:
    # name: buttons, breed: tabby etc 
  })

class SignUp(generic.CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('home')
  template_name = 'registration/signup.html'
  
  def form_valid(self, form):
    view = super(SignUp, self).form_valid(form)
    username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
    user - authenticate(username=username, password=password)
    login(self.request, user)
    return view
  
  
  
#Oh CRUD
class CreatePlaylist(generic.CreateView):
  model = Playlist
  fields = ['title']
  template_name = 'playlist/create_playlist.html'
  success_url = reverse_lazy('home')
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    super(CreatePlaylist, self).form_valid(form)
    return redirect('home')
    
class DetailPlaylist(generic.DetailView):
  model = Playlist
  template_name = 'playlist/detail_playlist.html'
  
class UpdatePlaylist(generic.UpdateView):
  model = Playlist
  template_name = 'playlist/update_playlist.html'
  fields = ['title']
  
class DeletePlaylist(generic.DeleteView):
  model = Playlist
  template_name = 'playlist/delete_playlist.html'