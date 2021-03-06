# Generated by Django 3.2.12 on 2022-02-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libido_contents", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="dislike_count",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="content",
            name="like_count",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="content",
            name="thumb_url",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="content",
            name="view_count",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
