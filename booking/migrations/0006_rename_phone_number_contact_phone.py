# Generated by Django 4.1 on 2022-08-14 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
