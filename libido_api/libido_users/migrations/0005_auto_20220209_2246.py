# Generated by Django 3.2.12 on 2022-02-09 13:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('libido_users', '0004_auto_20220209_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfriend',
            name='approved_at',
        ),
        migrations.RemoveField(
            model_name='myfriend',
            name='deleted_at',
        ),
        migrations.AlterField(
            model_name='myfriend',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime, help_text='친구초대 요청시간', verbose_name='친구초대 요청 시간'),
        ),
        migrations.AlterField(
            model_name='myfriend',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='친구요청 수락 상태', verbose_name='수락 상태'),
        ),
        migrations.AddConstraint(
            model_name='myfriend',
            constraint=models.UniqueConstraint(fields=('user', 'friend'), name='unique_status'),
        ),
    ]