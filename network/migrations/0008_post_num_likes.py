# Generated by Django 4.1.3 on 2022-11-25 05:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_post_num_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_likes',
            field=models.ManyToManyField(related_name='posts_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
