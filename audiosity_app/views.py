from .models import Song, Image
from django.core.paginator import Paginator
from .lyrics_processing import processing
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

import os
from django.conf import settings
from django.db.models import Q

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .forms import ImageForm
from django.shortcuts import get_object_or_404, redirect
from Image_2_text.image_2_text import generate_blip_caption

root_path = settings.BASE_DIR

def index(request):
    return HttpResponse("Hello, world. You're at the audiosity_app index.")

def home(request):
    return render(request, 'home.html')

def lyrics_analysis(request):
    return render(request, 'lyrics_analysis.html')

def lyrics2image(request):
    return render(request, 'lyrics2image.html')

def archive(request):
    query = request.GET.get('q', '')
    
    # Build the query filters
    if query:
        songs = Song.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        ).order_by('title')  # Example ordering by title, change as needed
    else:
        songs = Song.objects.all().order_by('title')  # Example ordering by title

    print(f"Number of songs fetched: {songs.count()}")
    print(f"Raw SQL Query: {str(songs.query)}")

    paginator = Paginator(songs, 20)  # Show 20 songs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'archive.html', {'page_obj': page_obj, 'query': query})

def lyrics_analysis(request):

    query = request.GET.get('query', '')

    print(query)

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.load_local(os.path.join(root_path, "audiosity_app/vector_db_lyrics_all_songs"), embedding, allow_dangerous_deserialization=True)

    docs = db.similarity_search(query,k=5)

    print(docs[0])

    result_docs = []

    for x in docs:
        temp = dict({'source':x.metadata['source'],
                     'content':x.page_content})
        result_docs.append(temp)

    #categs = Category.objects.all()[1:5]

    result_docs = processing(query,result_docs)
    print(result_docs)

    ctx = {
    #    'categories':categs,
        'results':result_docs
    }

    return render(request, 'lyrics_analysis.html', ctx)

def image2lyrics(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Speichere das Bild
            form.save()
            # Hole das neueste Bildobjekt, um es im Template anzuzeigen
            img_obj = form.instance
            # Redirect zur selben Seite, um ein erneutes Absenden des Formulars beim Aktualisieren zu verhindern
            return render(request, 'image2lyrics.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    
    # Hole das neueste Bildobjekt, um es im Template anzuzeigen (falls vorhanden)
    img_obj = None

    return render(request, 'image2lyrics.html', {'form': form, 'img_obj': img_obj})

def process_image(request, img_id):
    """Verarbeitet das Bild und gibt die Bildunterschrift als JSON zurück."""
    img_obj = get_object_or_404(Image, id=img_id)
    
    # Rufe die Bildverarbeitungsfunktion auf
    caption = generate_blip_caption(img_obj.image.path)
    
    # Gibt die Bildunterschrift als JSON zurück
    return HttpResponse(caption, content_type='text/plain')

def processing(request, img_id):
    """Zeigt das verarbeitete Bild an."""
    img_obj = get_object_or_404(Image, id=img_id)
    
    return render(request, 'processing.html', {'img_obj': img_obj})