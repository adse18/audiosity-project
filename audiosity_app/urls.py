from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('lyrics_analysis/', views.lyrics_analysis, name='lyrics_analysis'),
    path('lyrics2image/', views.lyrics2image, name='lyrics2image'),
    path('image2lyrics/', views.image2lyrics, name='image2lyrics'),
    path('image2lyrics/upload_image/', views.upload_image, name='upload_image'),

    path('archive/', views.archive, name='archive'),
]

