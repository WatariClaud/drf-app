# Generated by Django 4.1.5 on 2023-01-14 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_car_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='count',
        ),
        migrations.RemoveField(
            model_name='car',
            name='created',
        ),
        migrations.RemoveField(
            model_name='car',
            name='hire',
        ),
        migrations.RemoveField(
            model_name='car',
            name='registration_number',
        ),
        migrations.RemoveField(
            model_name='car',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='car',
            name='user_id',
        ),
    ]