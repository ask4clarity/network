# Generated by Django 3.1.3 on 2022-02-09 02:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='Likes',
            field=models.ManyToManyField(related_name='liker', to=settings.AUTH_USER_MODEL),
        ),
    ]
