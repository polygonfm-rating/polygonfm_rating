from django.conf.urls import include, url
from django.contrib import admin

from . import views
import rating.views.rating

urlpatterns = [
    url(r'^$', views.index, name='index'),
        # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^rating/', include('rating.urls')),
    url(r'rating/russian', rating.views.rating.russian_artists),
    url(r'rating/foreign', rating.views.rating.russian_artists),
    url(r'^admin/', include(admin.site.urls)),
]