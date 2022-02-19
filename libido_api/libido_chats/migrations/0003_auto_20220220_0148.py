# Generated by Django 3.2.12 on 2022-02-19 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("libido_chats", "0002_message_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="username",
        ),
        migrations.AddField(
            model_name="message",
            name="nickname",
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]