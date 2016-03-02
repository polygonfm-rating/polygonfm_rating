from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.conf.urls import url
from functools import update_wrapper
from rating.forms import UploadArtistsForm
from .models import *
import rating.utils.file


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'youtube_channel_id', 'is_russian', 'is_band', 'is_active')
    list_filter = ('is_russian', 'is_band', 'is_active')
    search_fields = ('name', )

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        base_urls = super(ArtistAdmin, self).get_urls()
        new_urls = [url(r'^upload/$', wrap(self.upload_file_view), name="upload"), ]
        return new_urls + base_urls

    def upload_file_view(self, request, extra_context=None):
        super(ArtistAdmin, self).changelist_view(request, extra_context)

        if request.method == "POST":
            form = UploadArtistsForm(request.POST, request.FILES)
            form.full_clean()

            # TODO handle validation errors
            if form.is_valid():
                f = request.FILES['artists_file']
                lines = rating.utils.file.read_uploaded_file(f)
                Artist.objects.create_from_list(lines)
                return HttpResponseRedirect('/admin/rating/artist/')

        return TemplateResponse(request, 'admin/rating/artist/upload.html', {'form':  UploadArtistsForm()})


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
