# Generated by Django 2.0.1 on 2018-02-08 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180208_1114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-like']},
        ),
    ]
