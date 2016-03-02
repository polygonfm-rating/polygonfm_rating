from datetime import datetime
from django.db import transaction
from django.db import models
from django.db.models.manager import Manager
from rating.utils import TimeElapsed
import uuid


class ArtistManager(Manager):
    def create_from_list(self, artists_to_create):
        to_save = []
        for artist in artists_to_create:
            if not self.filter(name=artist).exists():
                to_save.append(Artist(name=artist))

        with transaction.atomic():
            with TimeElapsed() as t:
                self.bulk_create(to_save)
                print("{} Artists from file saved in {} sec".format(datetime.now(), t.elapsed()))


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    youtube_channel_id = models.CharField(max_length=200, blank=True)
    is_russian = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_band = models.BooleanField(default=True)
    objects = ArtistManager()


class SessionState(models.Model):
    session = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)


class VkArtistRating(models.Model):
    session = models.ForeignKey(SessionState, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tracks_count = models.IntegerField(default=0)
    in_popular_count = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)


class VkPopularsSet(models.Model):
    artist_name = models.CharField(max_length=200)


class Rating(models.Model):
    session = models.ForeignKey(SessionState, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rank = models.FloatField(default=0)
    date = models.DateTimeField()


