from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Categories(models.Model):
    title = models.CharField('Название', max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    title = models.CharField("Название", max_length = 50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Категория")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегория"

    def str(self):
        return self.title


class Products(models.Model):
    title = models.CharField('Название', max_length=150, unique=True)
    quantity = models.PositiveIntegerField('Количество')
    image = models.ImageField(upload_to='products/')
    description = models.TextField('Описание')
    price = models.DecimalField(verbose_name='Цена', max_digits=100, decimal_places=2)
    discount = models.PositiveSmallIntegerField('Скидка', null=True, blank=True, default=0)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, verbose_name='Категория')
    subcategory = models.ForeignKey(SubCategories, on_delete=models.PROTECT, verbose_name='СубКатегория', null=True, blank=True)
    favorites = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ['-discount', '-favorites']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда к рейтингу"
        verbose_name_plural = "Звезды к рейтингу"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP Адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    products = models.ForeignKey(Products, on_delete=models.CharField, verbose_name="Продукт")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

  
class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    text = models.TextField('Комметарий')
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    star = models.ForeignKey(RatingStar, on_delete=models.CharField, verbose_name="Звезды", null=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.email)