# Generated by Django 3.2.12 on 2022-02-10 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import libido_commons.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='카테고리 이름', max_length=50, unique=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Created at')),
            ],
            options={
                'verbose_name': '카테고리',
                'verbose_name_plural': '카테고리 모음',
                'db_table': 'category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.CharField(db_index=True, default=libido_commons.utils._generate_random_token, max_length=45, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, help_text='타이틀', max_length=100, null=True)),
                ('description', models.TextField(blank=True, help_text='방 설명', null=True)),
                ('is_public', models.BooleanField(default=True, help_text='공개방 여부')),
                ('password', models.CharField(help_text='비밀번호', max_length=250)),
                ('user_count', models.PositiveIntegerField(blank=True, default=0, help_text='접속한 사람수', null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '방',
                'verbose_name_plural': '방 모음',
                'db_table': 'room',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('category', models.ForeignKey(blank=True, help_text='카테고리', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='roomcategory_category', to='libido_rooms.category')),
                ('room', models.ForeignKey(blank=True, help_text='스트리밍 방', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='roomcategory_room', to='libido_rooms.room')),
            ],
            options={
                'verbose_name': '방 카테고리',
                'verbose_name_plural': '방 카테고리 모음',
                'db_table': 'room_category',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='room',
            name='category',
            field=models.ManyToManyField(blank=True, help_text='룸 카테고리들', null=True, through='libido_rooms.RoomCategory', to='libido_rooms.Category'),
        ),
        migrations.AddField(
            model_name='room',
            name='moderator',
            field=models.ForeignKey(blank=True, help_text='방장(모더레이터)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_moderator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='roomcategory',
            constraint=models.UniqueConstraint(fields=('category', 'room'), name='unique_category_room'),
        ),
    ]