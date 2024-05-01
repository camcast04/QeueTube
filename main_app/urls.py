from django.urls import path
from . import views # . means from current file (main_app)
from django.conf.urls.static import static 



urlpatterns = [
  path('', views.home, name='home'), #making home controller -> now need to create the homes view in views.py
  path('about/', views.about, name='about'),
  path('playlists/', views.playlists_index, name='index'),
]

