# Generated by Django 4.2.5 on 2023-10-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingsettings',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
