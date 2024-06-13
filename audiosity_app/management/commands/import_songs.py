# music/management/commands/import_songs.py
import csv
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from ...models import Song

class Command(BaseCommand):
    help = 'Import songs from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row_number, row in enumerate(reader, start=1):
                try:
                    # Ensure all indices match your CSV structure
                    (album, album_url, artist, featured_artists_json,
                     lyrics, media_json, rank, release_date,
                     song_title, song_url, writers_json, year_str,
                     verbs, nouns, adverbs, corpus, word_counts,
                     unique_word_counts) = row

                    # Example: Parse release_date to date object
                    try:
                        release_date = datetime.strptime(release_date, '%Y-%m-%d').date() if release_date.strip() else None
                    except ValueError:
                        release_date = None  # or handle the error as per your logic

                    # Example: Convert year from string to integer
                    try:
                        year = int(float(year_str)) if year_str.strip() else None  # Convert '2013.0' to 2013 as integer
                    except ValueError:
                        year = None  # or handle the error as per your logic

                    # Example: Handle JSON fields
                    if featured_artists_json.strip():
                        try:
                            featured_artists_list = json.loads(featured_artists_json)
                        except json.JSONDecodeError as e:
                            self.stderr.write(self.style.ERROR(f'Error parsing featured_artists_json in row {row_number}: {e}'))
                            featured_artists_list = []  # or handle the error as per your logic
                    else:
                        featured_artists_list = []

                    if writers_json.strip():
                        try:
                            writers_list = json.loads(writers_json)
                        except json.JSONDecodeError as e:
                            self.stderr.write(self.style.ERROR(f'Error parsing writers_json in row {row_number}: {e}'))
                            writers_list = []  # or handle the error as per your logic
                    else:
                        writers_list = []

                    if media_json.strip():
                        try:
                            media_list = json.loads(media_json)
                        except json.JSONDecodeError as e:
                            self.stderr.write(self.style.ERROR(f'Error parsing media_json in row {row_number}: {e}'))
                            media_list = []  # or handle the error as per your logic
                    else:
                        media_list = []

                    # Example: Handle nullable fields like adverbs
                    adverbs = adverbs if adverbs.strip() else None

                    # Example: Create Song instance and save
                    song = Song(
                        album=album,
                        album_url=album_url,
                        artist=artist,
                        lyrics=lyrics,
                        rank=int(rank),
                        release_date=release_date,
                        song_title=song_title,
                        song_url=song_url,
                        year=year,
                        verbs=verbs,
                        nouns=nouns,
                        adverbs=adverbs,
                        corpus=corpus,
                        word_counts=int(word_counts),
                        unique_word_counts=int(unique_word_counts)
                    )
                    song.featured_artists_list = featured_artists_list
                    song.writers_list = writers_list
                    song.media_list = media_list
                    song.save()

                except IndexError as e:
                    self.stderr.write(self.style.ERROR(f'Error parsing row {row_number}: {e}'))
                    continue
                except ValueError as e:
                    self.stderr.write(self.style.ERROR(f'Error converting value in row {row_number}: {e}'))
                    continue
                except json.JSONDecodeError as e:
                    self.stderr.write(self.style.ERROR(f'Error parsing JSON in row {row_number}: {e}'))
                    continue
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error processing row {row_number}: {e}'))
                    continue

        self.stdout.write(self.style.SUCCESS('Successfully imported songs'))
