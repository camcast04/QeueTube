from django.urls import path
from . import views # . means from current file (main_app)




urlpatterns = [
  path('', views.home, name='home'), #making home controller -> now need to create the homes view in views.py
]