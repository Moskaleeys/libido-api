# Generated by Django 3.2.12 on 2022-02-16 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("libido_rooms", "0007_room_platform"),
        ("libido_users", "0008_invitation"),
    ]

    operations = [
        migrations.AddField(
            model_name="invitation",
            name="room",
            field=models.ForeignKey(
                blank=True,
                help_text="스트리밍 방",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invitation_room",
                to="libido_rooms.room",
            ),
        ),
    ]
