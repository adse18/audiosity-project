from django.shortcuts import render
from django.http import HttpResponse
from .models import Song
from django.core.paginator import Paginator

from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

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
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(song_title__icontains=query)
        songs = Song.objects.filter(artist__icontains=query)

    else:
        songs = Song.objects.all()

    paginator = Paginator(songs, 20)  # Show 20 songs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'archive.html', {'page_obj': page_obj, 'query': query})

def lyrics_analysis(request):

    query = request.GET.get('query', '')

    print(query)

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.load_local("C:/Users/Adrian/Documents/DHBW/6.Semester/advanced-ml/audiosity_root/audiosity_app/vector_db_lyrics", embedding, allow_dangerous_deserialization=True)

    docs = db.similarity_search(query,k=5)

    print(docs[0])

    result_docs = []

    for x in docs:
        temp = dict({'source':x.metadata['source'],
                     'content':x.page_content})
        result_docs.append(temp)

    #categs = Category.objects.all()[1:5]

    print(result_docs[0])

    ctx = {
    #    'categories':categs,
        'results':result_docs
    }

    return render(request, 'lyrics_analysis.html', ctx)