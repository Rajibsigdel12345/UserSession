# Generated by Django 5.1 on 2024-08-25 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_connection'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Connection',
        ),
    ]
