from django.db import models
from users.models import CustomUser


class Ingredient(models.Model):
    title = models.CharField(
        'Название',
        max_length=100
    )
    count = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10
    )


class Tag(models.Model):
    title = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', unique=True)
    hex_code = models.CharField('Цветовой код', max_length=7)


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    title = models.CharField(
        'Название',
        max_length=100
    )
    image = models.ImageField('Картинка')
    description = models.TextField('Текстовое описание')
    ingredient = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    time_for_preparing = models.TimeField('Время приготовления')
