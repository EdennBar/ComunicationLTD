# Generated by Django 4.2 on 2023-04-28 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_users_date_created_alter_users_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='date_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
