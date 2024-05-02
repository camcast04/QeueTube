# queuetube/main_app/urls.py

from django.urls import path
from . import views # . means from current file (main_app)
from django.conf.urls.static import static 




urlpatterns = [
  path('', views.home, name='home'), #making home controller -> now need to create the homes view in views.py
  path('about/', views.about, name='about'),
  path('dashboard/', views.dashboard, name='dashboard'),

  
  #playlist specific:
  path('playlists/create', views.CreatePlaylist.as_view(), name='create_playlist'),
  path('playlists/<int:pk>', views.DetailPlaylist.as_view(), name='detail_playlist'),
  path('playlists/<int:pk>/update', views.UpdatePlaylist.as_view(), name='update_playlist'),
  path('playlists/<int:pk>/delete', views.DeletePlaylist.as_view(), name='delete_playlist'),
  
  #Video killed the radio star 
  path('video/<int:pk>/addvideo', views.add_video, name='delete_playlist'),
  
  
]

