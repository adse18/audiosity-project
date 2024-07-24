import json
from django.db import models

class Song(models.Model):
    song_id = models.CharField(max_length=36, primary_key=True, default=0)
    album = models.CharField(max_length=200, default='Unknown Album')
    artist = models.CharField(max_length=200, default='Unknown Artist')
    title = models.CharField(max_length=200, default='Untitled')
    release_date = models.DateField(null=True, blank=True)
    lyrics = models.TextField(default='')

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

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return f"Image {self.id}"