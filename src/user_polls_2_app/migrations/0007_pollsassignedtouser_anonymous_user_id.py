# Generated by Django 3.2.7 on 2021-10-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_polls_2_app', '0006_alter_useranswer_anonymous_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollsassignedtouser',
            name='anonymous_user_id',
            field=models.UUIDField(blank=True, default=None, null=True, unique=True),
        ),
    ]
