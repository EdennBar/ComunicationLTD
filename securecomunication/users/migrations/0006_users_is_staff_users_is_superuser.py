# Generated by Django 4.2 on 2023-04-28 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_users_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
