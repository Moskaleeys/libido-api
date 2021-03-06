# Generated by Django 3.2.12 on 2022-02-10 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libido_rooms', '0003_alter_room_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='deleted_at',
            field=models.DateTimeField(blank=True, db_index=True, default=None, help_text='탈퇴 또는 삭제한 시간', null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='is_public',
            field=models.BooleanField(db_index=True, default=True, help_text='공개방 여부'),
        ),
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.CharField(blank=True, db_index=True, help_text='타이틀', max_length=100, null=True),
        ),
    ]
