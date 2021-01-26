# Generated by Django 3.1.4 on 2020-12-18 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='items',
        ),
        migrations.AddField(
            model_name='comments',
            name='item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.createlist'),
        ),
    ]