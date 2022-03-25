from django.db import models
from backend.apps.shop.models import Products

# Create your models here.

class Order(models.Model):
    fio = models.CharField('ФИО', max_length=150)
    phone_number = models.CharField('Номер телефона', max_length=150)
    email = models.EmailField('Электронная почта')
    address = models.CharField('Адрес', max_length=200)
    post_code = models.CharField('Почтовый Индекс', max_length=200)
    total_sum = models.DecimalField("Общая сумма",max_digits=10, decimal_places=2)
    bank_card = models.CharField('Банковская карта', max_length=20)
    status = models.BooleanField(default=False)
    created = models.DateTimeField("Создание", auto_now_add=True, db_index=True)
    

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['created']



class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.DO_NOTHING)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return self.product.title

