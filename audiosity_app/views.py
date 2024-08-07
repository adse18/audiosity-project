from .models import Song, Image
from django.core.paginator import Paginator
from .lyrics_processing import lyrics_processing
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from .forms import ImageForm
from django.shortcuts import get_object_or_404, redirect, render
from audiosity_app.utils.image_2_text import generate_blip_caption
import json
from django.views.decorators.csrf import csrf_exempt

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
    result_docs = []

    # Only load the vector store and perform the search if a query is provided
    if query:
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(os.path.join(root_path, "audiosity_app/vector_db_lyrics_all_songs"), embedding, allow_dangerous_deserialization=True)
        docs = db.similarity_search(query, k=5)
        
        for x in docs:
            temp = dict({
                'source': x.metadata['source'],
                'content': x.page_content
            })
            result_docs.append(temp)
        result_docs = lyrics_processing(query, result_docs)

    ctx = {
        'results': result_docs
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

@csrf_exempt
def search_lyrics(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('caption', '')
        result_docs = []
        
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = FAISS.load_local(os.path.join(root_path, "audiosity_app/vector_db_lyrics_all_songs"), embedding, allow_dangerous_deserialization=True)
        docs = db.similarity_search(query, k=1)
        
        if docs:
            doc = docs[0]
            title, artist = doc.metadata['source'] 
            result = f"{title} by: {artist}"
            return JsonResponse({'result': result})
        
        return JsonResponse({'result': 'No results found'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
