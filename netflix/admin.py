from django.contrib import admin
from django.utils.html import format_html

from netflix.models import Movie
from netflix.models import Category
from netflix.models import Tag

admin.site.register(Category)
admin.site.register(Tag)


class MovieAdmin(admin.ModelAdmin):

    def preview(self, movie):
        """Render preview image as html image."""

        return format_html(
            f'<img style="height: 200px" src="/media/{movie.preview_image}" />'
        )

    def video(self, movie):
        """Render movie video as html image."""

        return format_html(
            '''
            <video width="320" height="240" controls>
                <source src="%s" type="video/mp4">
                Your browser does not support the video tag.
            </video>''' % movie.file
        )

    preview.short_description = 'Movie image'
    video.short_description = 'Movie video'
    list_display = ['name', 'preview', 'video', 'description']

admin.site.register(Movie, MovieAdmin)
