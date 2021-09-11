# Generated by Django 3.2.5 on 2021-09-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booksreviews', '0003_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='カテゴリ名')),
                ('name_en', models.CharField(max_length=50, verbose_name='カテゴリ名英語')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
