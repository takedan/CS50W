# Generated by Django 3.1.4 on 2020-12-16 00:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_delete_createlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('CategoryID', models.AutoField(primary_key=True, serialize=False)),
                ('Category', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CreateList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('imageurl', models.URLField()),
                ('datecreation', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='auctions.itemcategory')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
