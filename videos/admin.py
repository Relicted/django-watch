from django.contrib import admin
from .models import (
    Video,
    VideoScreenshot,
    VideoFile,
    Season,
    WatchingList,
    Genre
)
from .forms import CreateVideoItemForm
# Register your models here.
admin.site.register(Genre)
admin.site.register(WatchingList)


class VideoSeasonTabularInline(admin.TabularInline):
    model = Season
    extra = 0


class VideoScreenshotTabularInline(admin.TabularInline):
    model = VideoScreenshot
    extra = 0


class VideoAdmin(admin.ModelAdmin):
    list_display = ['original_title', 'content', 'id']
    inlines = [
        VideoScreenshotTabularInline,
        VideoSeasonTabularInline
    ]
    class Meta:
        model = Video


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoScreenshot)

admin.site.register(VideoFile)