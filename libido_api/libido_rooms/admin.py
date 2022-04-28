from django.contrib import admin
from libido_rooms.models import Room, Category, RoomCategory
from libido_contents.models import Content

# Register your models here.


class CategoryTemplateInline(admin.TabularInline):
    extra = 0
    autocomplete_fields = ["category"]
    model = Room.category.through
    show_change_link = True


class ContentInline(admin.TabularInline):
    extra = 0
    autocomplete_fields = ["content"]
    exclude = [
        "title",
        "thumb",
        "url",
        "published_at",
        "created_at",
        "deleted_at",
    ]

    show_change_link = True
    model = Room.contents.through


class RoomAdmin(admin.ModelAdmin):
    inlines = [CategoryTemplateInline, ContentInline]
    autocomplete_fields = ["moderator"]
    search_fields = ["title", "desctiption", "moderator"]
    list_display = [
        "id",
        "title",
        "is_public",
        "moderator",
        "user_count",
        "created_at",
    ]
    list_display_links = [
        "id",
        "title",
        "is_public",
        "moderator",
        "user_count",
        "created_at",
    ]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = [
        "id",
        "name",
        "created_at",
    ]
    list_display_links = [
        "id",
        "name",
        "created_at",
    ]


class RoomCategoryAdmin(admin.ModelAdmin):
    search_fields = ["category", "room"]
    autocomplete_fields = ["category", "room"]
    list_display = [
        "id",
        "category",
        "room",
        "created_at",
    ]
    list_display_links = [
        "id",
        "category",
        "room",
        "created_at",
    ]


admin.site.register(Room, RoomAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(RoomCategory, RoomCategoryAdmin)
