# Generated by Django 3.2.7 on 2021-09-23 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user_app', '0002_auto_20210919_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
