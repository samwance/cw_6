# Generated by Django 4.2.5 on 2023-10-13 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('title', models.CharField(max_length=100,
                                           verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('preview_image', models.ImageField(
                    blank=True,
                    null=True,
                    upload_to='blog_images/',
                    verbose_name='Изображение')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True,
                    verbose_name='Дата создания')
                 ),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='Опубликовано')
                 ),
                ('views_count', models.PositiveIntegerField(
                    default=0,
                    verbose_name='Количество просмотров')
                 ),
            ],
            options={
                'verbose_name': 'запись',
                'verbose_name_plural': 'записи',
            },
        ),
    ]
