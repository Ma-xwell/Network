# Generated by Django 4.1.6 on 2023-06-29 21:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(default='self', null=True, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
    ]