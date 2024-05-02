from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Playlist

# Basic Views
class HomeView(generic.TemplateView):
    template_name = 'home.html'

class DashboardView(generic.TemplateView):
    template_name = 'dashboard.html'

class AboutView(generic.TemplateView):
    template_name = 'about.html'

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

class CreatePlaylist(generic.CreateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/create_playlist.html'
    success_url = reverse_lazy('home')
  
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DetailPlaylist(generic.DetailView):
    model = Playlist
    template_name = 'playlist/detail_playlist.html'

class UpdatePlaylist(generic.UpdateView):
    model = Playlist
    fields = ['title']
    template_name = 'playlist/update_playlist.html'
    success_url = reverse_lazy('dashboard')

class DeletePlaylist(generic.DeleteView):
    model = Playlist
    template_name = 'playlist/delete_playlist.html'
    success_url = reverse_lazy('dashboard')
