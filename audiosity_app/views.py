from django.shortcuts import render
from django.http import HttpResponse
from .models import Song
from django.core.paginator import Paginator

def index(request):
    return HttpResponse("Hello, world. You're at the audiosity_app index.")

def home(request):
    return render(request, 'home.html')

def lyrics_analysis(request):
    return render(request, 'lyrics_analysis.html')

def lyrics2image(request):
    return render(request, 'lyrics2image.html')

def image2lyrics(request):
    return render(request, 'image2lyrics.html')

def archive(request):
    query = request.GET.get('q')
    if query:
        songs = Song.objects.filter(title__icontains=query)
    else:
        songs = Song.objects.all()

    paginator = Paginator(songs, 10)  # Show 10 songs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'archive.html', {'page_obj': page_obj, 'query': query})