# Generated by Django 3.2.12 on 2022-02-07 16:53

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields
import libido_commons.utils
import libido_users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.CharField(db_index=True, default=libido_commons.utils._generate_random_token, max_length=40, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True, help_text='액티브된 유저 유무 확인 is_active 가 false로 된경우 accesstoken을 받아올 수 없다.', verbose_name='활성화 상태')),
                ('is_recruiter', models.BooleanField(default=False, help_text='리쿠르터 여부', verbose_name='리쿠르터 여부')),
                ('nickname', models.CharField(blank=True, help_text='외부 노출되는 이름(닉네임)', max_length=50, null=True, verbose_name='외부 노출 닉네임')),
                ('date_of_birth', models.DateField(blank=True, help_text='생일', null=True)),
                ('bio', models.TextField(blank=True, default=None, help_text='자기소개', max_length=3000, null=True, verbose_name='Bio')),
                ('thumb', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=libido_users.models.upload_thumb)),
                ('mobile', models.CharField(blank=True, help_text='핸드폰 번호', max_length=50, null=True, verbose_name='핸드폰 번호')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, help_text='가장 최근 로그인 한 시간', verbose_name='최근 로그인 한 시간')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='유저를 최초 가입 또는 생성한 시간', verbose_name='가입 한 날짜 및 시간')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='Updated at')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, help_text='탈퇴 또는 삭제한 시간', null=True, verbose_name='탈퇴 또는 삭제한 시간')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자 모음',
                'db_table': 'user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
