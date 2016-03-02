from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts rating data collection process'

    def handle(self, *args, **options):
        import ratingservice
        ratingservice.execute_collect_rating()
