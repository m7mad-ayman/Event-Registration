# Generated by Django 4.2.3 on 2024-09-06 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_registration_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='available',
            field=models.IntegerField(null=True),
        ),
    ]
