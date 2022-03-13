from django.db import models
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from libido_commons.models import PrintableModel


class Message(PrintableModel):
    nickname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(),
        verbose_name="사용자",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_user",
        help_text="유저",
    )

    room = models.ForeignKey(
        "libido_rooms.Room",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="message_room",
        help_text="스트리밍 방",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        verbose_name="작성한 시간",
        db_index=True,
        default=timezone.now,
        help_text="메세지 작성한 시간",
    )

    def __str__(self):
        return f"{self.nickname}"

    class Meta:
        ordering = ["-id"]
        verbose_name = "채팅 메세지"
        verbose_name_plural = "채팅 메세지 모음"
        db_table = "message"
        managed = True
