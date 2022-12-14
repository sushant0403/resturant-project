# Generated by Django 4.1.1 on 2022-10-12 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('Cat_image', models.ImageField(blank=True, upload_to='static/images')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Dishes_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish_name', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=200, null=True, unique=True)),
                ('ingredients', models.TextField(blank=True, max_length=200, null=True, unique=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='static/images')),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category')),
            ],
            options={
                'verbose_name': 'Dish',
                'verbose_name_plural': 'Dishes',
            },
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField(blank=True, max_length=500)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.dishes_model')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
