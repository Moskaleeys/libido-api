# Generated by Django 3.2.12 on 2022-02-09 13:05

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('libido_users', '0002_auto_20220208_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(blank=True, help_text='국가 필드', max_length=2, null=True),
        ),
    ]
