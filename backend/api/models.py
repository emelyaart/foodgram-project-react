from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    name = models.CharField(
        'Название',
        max_length=100
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=10
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    BLUE = '#4A61DD'
    ORANGE = '#E26C2D'
    GREEN = '#49B64E'
    PURPLE = '#8775D2'
    YELLOW = '#F9A62B'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый')
    ]

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', unique=True)
    color = models.CharField(
        'Цветовой код',
        max_length=7,
        choices=COLOR_CHOICES
    )

    def __str__(self):
        return self.name


class Subscribe(models.Model):

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )


class Recipe(models.Model):

    class Meta:
        ordering = ['id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    name = models.CharField(
        'Название',
        max_length=100
    )
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.IntegerField('Время приготовления')

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.SmallIntegerField('Количество')


class Favorite(models.Model):

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class Cart(models.Model):

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )
