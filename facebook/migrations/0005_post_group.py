# Generated by Django 3.1.5 on 2021-01-12 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0004_message_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ManyToManyField(to='facebook.Groups'),
        ),
    ]