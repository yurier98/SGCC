# Generated by Django 4.1.2 on 2023-11-27 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='number',
        ),
    ]
