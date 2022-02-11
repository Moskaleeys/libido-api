from django.contrib import admin
from libido_contents.models import Content


class ContentAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = [
        "id",
        "title",
        "thumb",
        "channel_id",
        "channel_title",
        "running_time",
        "created_at",
        "published_at",
        "deleted_at",
    ]
    list_display_links = [
        "id",
        "title",
        "thumb",
        "channel_id",
        "channel_title",
        "running_time",
        "created_at",
        "published_at",
        "deleted_at",
    ]


admin.site.register(Content, ContentAdmin)
