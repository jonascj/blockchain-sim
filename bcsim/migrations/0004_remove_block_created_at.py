# Generated by Django 3.2.8 on 2021-10-18 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bcsim', '0003_delete_blockchain2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='created_at',
        ),
    ]
