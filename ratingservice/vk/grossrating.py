import time
from rating.utils import TimeElapsed
from datetime import datetime
from django.db import transaction
from vk.exceptions import VkAPIError
from ratingservice.vk import VkService
from rating.models import Artist, VkArtistRating, VkPopularsSet


class VkGrossRatingService(VkService):
    def __init__(self, session_state):
        super().__init__()
        self.session = session_state

    def collect(self):
        print("{} START: VK rating service".format(datetime.now()))

        with TimeElapsed() as t:
            artists = Artist.objects.all().filter(is_active=True)[0:20]
            print("{} VK Artists count: {}".format(datetime.now(), len(artists)))

            with TimeElapsed() as t1:
                #i = 1
                to_save = []
                for artist in artists:
                    in_popular_count = self.__get_in_popular_count(artist)
                    # print("{} {} {} __get_tracks_count".format(datetime.now(), i, artist.name))
                    # i += 1
                    # tracks = self.__get_tracks_count(artist)
                    tracks = 0
                    if tracks > 0 or in_popular_count > 0:
                        p = VkArtistRating(artist=artist, tracks_count=tracks, in_popular_count=in_popular_count,
                                           session=self.session)
                        to_save.append(p)
                print("{} VK rating data collected in {}".format(datetime.now(), t1.elapsed()))

                VkArtistRating.objects.bulk_create(to_save)

            self.__calculate_gross_rating()
            print("{} COMPLETED: VK rating service in {}".format(datetime.now(), t.elapsed()))

    def get_ranked_artists(self):
        return VkArtistRating.objects.filter(session=self.session).order_by('rank')

    def __get_tracks_count(self, artist):
        return self.__call_vk_api(lambda: self.vkapi.audio.search(q=artist.name, performer_only=1, count=0)[0])

    def __get_in_popular_count(self, artist):
        return VkPopularsSet.objects.filter(artist_name__icontains=artist.name).count()

    def __call_vk_api(self, call, retry_count=3, sleep_time=1):
        try:
            time.sleep(0.5)
            return call()
        except VkAPIError as e:
            if e.is_captcha_needed() and retry_count > 0:
                print("{} Captcha needed".format(datetime.now()))
                if retry_count == 3:
                    sleep_time = 360
                time.sleep(sleep_time)
                print("{} Retry".format(datetime.now()))
                return self.__call_vk_api(call, retry_count - 1, sleep_time + 360)
            # if too many requests
            elif e.code == 6 and retry_count > 0:
                print("{} Too many requests".format(datetime.now()))
                time.sleep(sleep_time)
                print("{} Retry".format(datetime.now()))
                return self.__call_vk_api(call, retry_count - 1, sleep_time + 1)
            else:
                print("{} Exception: {}".format(datetime.now(), e.code))
                raise

    def __calculate_gross_rating(self):
        with TimeElapsed() as t:
            rank = 1
            with transaction.atomic():
                for item in list(VkArtistRating.objects.filter(session=self.session).
                                         order_by('-in_popular_count', '-tracks_count')):
                    item.rank = rank
                    item.save()
                    rank += 1
            print("{} VK gross rating counted in {}".format(datetime.now(), t.elapsed()))