
def execute_collect_rating():
    from ratingservice.coordinator import RatingServicesCoordinator
    RatingServicesCoordinator().execute()


def execute_vk_reload_popular_set():
    from ratingservice.vk.reloadpopulars import ReloadPopularsService
    ReloadPopularsService().reload_populars()
