# Generated by Django 3.2.12 on 2022-02-09 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import libido_commons.utils


class Migration(migrations.Migration):

    dependencies = [
        ('libido_users', '0003_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(db_index=True, default=libido_commons.utils._generate_random_token, max_length=45, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, help_text='액티브된 유저 유무 확인 is_active 가 false로 된경우 accesstoken을 받아올 수 없다.', verbose_name='활성화 상태'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, db_index=True, help_text='핸드폰 번호', max_length=50, null=True, verbose_name='핸드폰 번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, db_index=True, help_text='외부 노출되는 이름(닉네임)', max_length=50, null=True, verbose_name='외부 노출 닉네임'),
        ),
        migrations.CreateModel(
            name='MyFriend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(db_index=True, default=True, help_text='친구요청 수락 상태', verbose_name='수락 상태')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.localtime, help_text='친구초대 요청시간', verbose_name='친구초대 요청 시간')),
                ('approved_at', models.DateTimeField(db_index=True, help_text='친구초대 요청수락시간', verbose_name='친구초대 요청 수락')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, help_text='삭제한 시간', null=True, verbose_name='삭제한 시간')),
                ('friend', models.ForeignKey(blank=True, help_text='친구', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='myfriend_friend', to=settings.AUTH_USER_MODEL, verbose_name='친구')),
                ('user', models.ForeignKey(blank=True, help_text='유저', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='myfriend_user', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '친구',
                'verbose_name_plural': '친구 모음',
                'db_table': 'friend',
                'managed': True,
            },
        ),
    ]
