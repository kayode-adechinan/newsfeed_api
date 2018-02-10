# Generated by Django 2.0.1 on 2018-02-10 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='', verbose_name='Uploaded video')),
                ('picture', models.ImageField(null=True, upload_to=post.models.scramble_uploaded_filename, verbose_name='Uploaded image')),
                ('picture_thumbnail', models.ImageField(blank=True, upload_to='', verbose_name='Thumbnail of uploaded image')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255, null=True)),
                ('content', models.TextField()),
                ('rating', models.IntegerField(null=True)),
                ('like', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-like'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, upload_to=post.models.scramble_uploaded_filename, verbose_name='Uploaded image')),
                ('avatar_thumbnail', models.ImageField(blank=True, upload_to='', verbose_name='Thumbnail of uploaded image')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
    ]
