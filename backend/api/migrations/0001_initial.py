# Generated by Django 3.2.5 on 2021-07-13 16:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=10, verbose_name='Единица измерения')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(verbose_name='Количество')),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('color', models.CharField(max_length=7, verbose_name='Цветовой код')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Текстовое описание')),
                ('cooking_time', models.IntegerField(verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='api.IngredientAmount', to='api.Ingredient', verbose_name='Ингридиенты')),
                ('tags', models.ManyToManyField(to='api.Tag', verbose_name='Теги')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.recipe'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='api.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_cart', to='api.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
