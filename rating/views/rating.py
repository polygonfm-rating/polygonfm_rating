import json
from django.http import HttpResponse
from rating.models import Rating, SessionState


def russian_artists(request):
    return __artists(request, True)


def foreign_artists(request):
    return __artists(request, False)


def __artists(request, is_russian):
    last_session = SessionState.objects.filter(is_completed=True).order_by('date').first()
    artists = []
    for record in Rating.objects.filter(session=last_session,
                                        artist__is_russian=is_russian,
                                        artist__is_active=True,).order_by("rank")[0:50]:
        artists.append(record.artist.name)
    return HttpResponse(json.dumps(artists, ensure_ascii=False), content_type="application/json")

