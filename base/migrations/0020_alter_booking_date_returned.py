# Generated by Django 4.1.5 on 2023-01-22 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date_returned',
            field=models.DateTimeField(null=True),
        ),
    ]
