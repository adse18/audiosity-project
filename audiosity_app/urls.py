from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('lyrics_analysis/', views.lyrics_analysis, name='lyrics_analysis'),
    path('lyrics2image/', views.lyrics2image, name='lyrics2image'),
    path('image2lyrics/', views.image2lyrics, name='image2lyrics'),
    path('archive/', views.archive, name='archive'),
    path('process_image/<int:img_id>/', views.process_image, name='process_image'),
    path('processing/<int:img_id>/', views.processing, name='processing'),
    path('search_lyrics/', views.search_lyrics, name='search_lyrics'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

