# Generated by Django 4.2 on 2023-04-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_users_is_staff_remove_users_is_superuser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='users',
            name='date_joined',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
