# Generated by Django 5.1.6 on 2025-03-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jersi_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jersi',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
