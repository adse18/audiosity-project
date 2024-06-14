from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lyrics_analysis/', views.lyrics_analysis, name='lyrics_analysis'),
    path('lyrics2image/', views.lyrics2image, name='lyrics2image'),
    path('image2lyrics/', views.image2lyrics, name='image2lyrics'),
    path('archive/', views.archive, name='archive'),

]
