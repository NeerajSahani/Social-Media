# Generated by Django 3.1.5 on 2021-01-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook', '0005_post_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='members',
            field=models.ManyToManyField(related_name='group', to='facebook.Person'),
        ),
    ]