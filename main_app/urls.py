# queuetube/main_app/urls.py

from django.urls import path
from . import views # . means from current file (main_app)
from django.conf.urls.static import static 




urlpatterns = [
  path('', views.home, name='home'), #making home controller -> now need to create the homes view in views.py
  path('about/', views.about, name='about'),
  path('dashboard/', views.dashboard, name='dashboard'),

  
  #playlist specific:
  path('playlist/create', views.CreatePlaylist.as_view(), name='create_playlist'),
  path('playlist/<int:pk>', views.DetailPlaylist.as_view(), name='detail_playlist'),
  path('playlist/<int:pk>/update', views.UpdatePlaylist.as_view(), name='update_playlist'),
  path('playlist/<int:pk>/delete', views.DeletePlaylist.as_view(), name='delete_playlist'),
  path('playlists/', views.all_playlists, name='all_playlists'),
  path('user_playlists/<int:user_id>/', views.user_playlists, name='user_playlists'),

  
  #Video killed the radio star 
  path('video/<int:pk>/addvideo', views.add_video, name='add_video'),
  path('video/<int:pk>/delete', views.DeleteVideo.as_view(), name='delete_video'),
  path('video/search', views.video_search, name='video_search'),
  
  
]

