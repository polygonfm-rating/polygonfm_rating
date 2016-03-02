from django.db import transaction
from datetime import datetime
from ratingservice.vk import VkService
from rating.models import VkPopularsSet
from rating.utils import TimeElapsed


class ReloadPopularsService(VkService):

    def reload_populars(self):
        print("{} START: VK Reload popular artists".format(datetime.now()))
        with TimeElapsed() as t:
            self.__reload()
            print("{} COMPLETED: VK Reload popular artists in {}".format(datetime.now(), t.elapsed()))

    def __reload(self):
        with TimeElapsed() as t:
            populars = self.vkapi.execute.get_popular(only_eng=0)
            print("{} Popular artists retrieved from vk.com: {} items in {} sec".format(datetime.now(),
                                                                                        len(populars), t.elapsed()))
        with TimeElapsed() as t:
            to_file = dict()
            for artist in populars[:18000]:
                to_file[artist.strip()] = None

            with open("artists.txt", 'w', encoding='UTF-8') as f:
                [f.write(k + '\r\n') for k in to_file.keys()]
            print("{} File with artists written in {}. Total: {}".format(datetime.now(),
                                                                         t.elapsed(), len(to_file.keys())))

        to_save = [VkPopularsSet(artist_name=artist.strip()) for artist in populars]

        with transaction.atomic():
            VkPopularsSet.objects.all().delete()
            with TimeElapsed() as t:
                VkPopularsSet.objects.bulk_create(to_save)
                print("{} Popular artists saved in {} sec".format(datetime.now(), t.elapsed()))