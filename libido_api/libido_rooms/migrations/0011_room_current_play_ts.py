# Generated by Django 3.2.12 on 2022-03-17 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libido_rooms", "0010_auto_20220301_1322"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="current_play_ts",
            field=models.IntegerField(
                blank=True, help_text="현 재생중인 콘텐츠 타임스템프", null=True
            ),
        ),
    ]