# Generated by Django 3.2.13 on 2022-08-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_bookingrequest_bookingrequestitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='state',
            field=models.CharField(choices=[('booked', 'Booked'), ('in_used', 'In Used'), ('cleaning', 'Cleaning')], max_length=30),
        ),
    ]
