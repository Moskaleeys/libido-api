from django.contrib import admin
from libido_users.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ["username", "nickname"]
    list_display = [
        "id",
        "is_active",
        "username",
        "nickname",
        "created_at",
    ]
    list_display_links = [
        "id",
        "is_active",
        "username",
        "nickname",
        "created_at",
    ]


admin.site.register(User, UserAdmin)
admin.site.site_title = "리비도 어드dddd민 페이지"
admin.site.site_header = "리비도 어dddd드민"
admin.site.index_title = "리비도 어dddd드민 입니다."
