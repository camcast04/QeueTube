from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
  return render(request, 'home.html')

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