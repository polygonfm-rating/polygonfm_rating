from datetime import datetime
from rating.utils import TimeElapsed
from ratingservice.vk.grossrating import VkGrossRatingService
from ratingservice.vk.reloadpopulars import ReloadPopularsService
from rating.models import SessionState, Rating


class RatingServicesCoordinator:

    def execute(self):
        print("{} START: Collect artists rating".format(datetime.now()))
        with TimeElapsed() as t:
            session = SessionState.objects.create()
            session.save()

            vk_rating = VkGrossRatingService(session)
            vk_rating.collect()

            with TimeElapsed() as t1:
                self.__calculate_gross_rating(session, vk_rating)
                print("{} Gross rating counted in {}".format(datetime.now(), t1.elapsed()))

            session.is_completed = True
            session.save()

            print("{} COMPLETED: Artists rating successfully collected and counted in {}".format(datetime.now(), t.elapsed()))

    # Counts total artists rating collected from all services
    def __calculate_gross_rating(self, session, vk_rating):
            to_save = []
            for ranked in vk_rating.get_ranked_artists():
                to_save.append(Rating(session=session, artist=ranked.artist, rank=ranked.rank, date=session.date))

            Rating.objects.bulk_create(to_save)