# Generated by Django 5.0.6 on 2024-07-09 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0007_usersubscription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='Permissions',
            new_name='permissions',
        ),
        migrations.RenameField(
            model_name='usersubscription',
            old_name='Subscription',
            new_name='subscription',
        ),
    ]