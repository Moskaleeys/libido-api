from django.contrib import admin
from libido_contents.models import Content, Genre


class GenreTemplateInline(admin.TabularInline):
    extra = 0
    # autocomplete_fields = ["genre"]
    model = Content.genre.through
    show_change_link = True


class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name", "created_at"]
    list_display_links = ["id", "name", "created_at"]


class ContentAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    inlines = [GenreTemplateInline]
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
admin.site.register(Genre, GenreAdmin)
