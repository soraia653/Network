# Generated by Django 4.1.3 on 2022-11-12 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
