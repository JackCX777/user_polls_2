# Generated by Django 3.2.7 on 2021-10-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_polls_2_app', '0008_auto_20211025_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollsassignedtouser',
            name='anonymous_user_id',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='anonymous_user_id',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]