# Generated by Django 3.1.4 on 2020-12-18 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='createlist',
            name='bid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]