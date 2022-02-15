# Generated by Django 3.2.12 on 2022-02-13 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libido_rooms", "0005_auto_20220211_1426"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="play_lists_count",
            field=models.PositiveIntegerField(
                blank=True, default=0, help_text="플레이 리스트 카운트", null=True
            ),
        ),
    ]