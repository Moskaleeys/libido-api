# Generated by Django 3.2.12 on 2022-02-09 17:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os', models.CharField(blank=True, help_text='운영체', max_length=15, null=True, verbose_name='운영체제')),
                ('current_version', models.CharField(blank=True, help_text='현재 버전', max_length=15, null=True, verbose_name='현재 앱 버전')),
                ('min_version', models.CharField(blank=True, help_text='최소 버전', max_length=15, null=True, verbose_name='최소 버전')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
            ],
            options={
                'verbose_name': '앱 버전',
                'verbose_name_plural': '앱 버전 모음',
                'db_table': 'app_version',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MarketingConsent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='타이틀', max_length=300, null=True)),
                ('content', models.TextField(blank=True, default=None, help_text='콘텐츠', max_length=50000, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
            ],
            options={
                'verbose_name': '마케팅 수신동의',
                'verbose_name_plural': '마케팅 수신동의 모음',
                'db_table': 'marketing_consent',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='타이틀', max_length=300, null=True)),
                ('content', models.TextField(blank=True, default=None, help_text='콘텐츠', max_length=50000, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
            ],
            options={
                'verbose_name': '개인정보 처리방침',
                'verbose_name_plural': '개인정보 처리방침 모음',
                'db_table': 'privacy_policy',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TermsOfService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='타이틀', max_length=300, null=True)),
                ('content', models.TextField(blank=True, default=None, help_text='콘텐츠', max_length=50000, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, null=True)),
            ],
            options={
                'verbose_name': '이용 약관',
                'verbose_name_plural': '이용 약관 모음',
                'db_table': 'terms_of_service',
                'managed': True,
            },
        ),
    ]