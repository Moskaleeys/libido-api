# Generated by Django 3.2.12 on 2022-02-17 13:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libido_contents', '0004_auto_20220216_0114'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserContentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.PositiveIntegerField(blank=True, default=0, help_text='시청 분', null=True)),
                ('genre', models.CharField(blank=True, help_text='장르', max_length=20, null=True)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('content', models.ForeignKey(blank=True, help_text='콘텐츠', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usercontenthistoy_content', to='libido_contents.content')),
            ],
            options={
                'verbose_name': '사용자 콘텐츠 시청기록',
                'verbose_name_plural': '사용자 콘텐츠 시청기록 모음',
                'db_table': 'user_content_history',
                'managed': True,
            },
        ),
    ]