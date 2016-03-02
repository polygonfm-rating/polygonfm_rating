from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Reload set of popular artists from vk.api.audio.getPopular'

    def handle(self, *args, **options):
        import ratingservice
        ratingservice.execute_vk_reload_popular_set()
