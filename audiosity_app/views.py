from django.shortcuts import render
from django.http import HttpResponse

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