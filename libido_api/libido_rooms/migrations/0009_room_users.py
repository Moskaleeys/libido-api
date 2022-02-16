# Generated by Django 3.2.12 on 2022-02-16 13:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("libido_rooms", "0008_auto_20220216_2150"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                help_text="룸 참여자들",
                through="libido_rooms.RoomUser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
