# Generated by Django 4.1.6 on 2023-07-08 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_user_following_alter_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(related_name='user_liked', to='network.post'),
        ),
    ]
