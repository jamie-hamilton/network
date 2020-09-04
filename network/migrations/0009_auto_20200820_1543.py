# Generated by Django 3.0.8 on 2020-08-20 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20200820_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='users',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='follow', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='follow',
            name='current_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_list', to=settings.AUTH_USER_MODEL),
        ),
    ]
