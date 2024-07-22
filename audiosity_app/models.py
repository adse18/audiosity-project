# music/models.py
import json
from django.db import models

class Song(models.Model):
    song_id = models.CharField(max_length=36, primary_key=True, default=0)
    album = models.CharField(max_length=200, default='Unknown Album')  # Default value specified
    artist = models.CharField(max_length=200, default='Unknown Artist')  # Default value specified
    title = models.CharField(max_length=200, default='Untitled')  # Default value specified
    release_date = models.DateField(null=True, blank=True)  # Allows null and blank values
    lyrics = models.TextField(default='')  # Default empty string for lyrics
    # album_url = models.CharField(max_length=200)
    # featured_artists = models.TextField(default="[]")  # Store as JSON string
    # media = models.TextField(default="[]")  # Store as JSON string
    # rank = models.IntegerField(default=0)
    # song_url = models.CharField(max_length=200)
    # writers = models.TextField(default="[]")  # Store as JSON string
    # year = models.IntegerField(default=0)
    # verbs = models.TextField(default="")
    # nouns = models.TextField(default="")
    # adverbs = models.TextField(default="")  # Provide a default value
    # corpus = models.TextField(default="")
    # word_counts = models.IntegerField(default=0)
    # unique_word_counts = models.IntegerField(default=0)

    class Meta:
        db_table = 'songs'

    def __str__(self):
        return self.title

    @property
    def featured_artists_list(self):
        return json.loads(self.featured_artists)

    @featured_artists_list.setter
    def featured_artists_list(self, value):
        self.featured_artists = json.dumps(value)

    @property
    def writers_list(self):
        return json.loads(self.writers)

    @writers_list.setter
    def writers_list(self, value):
        self.writers = json.dumps(value)
