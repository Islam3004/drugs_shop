# Generated by Django 3.2.9 on 2022-03-22 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0021_remove_products_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=150, verbose_name='ФИО')),
                ('phone_number', models.CharField(max_length=150, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('post_code', models.CharField(max_length=200, verbose_name='Почтовый Индекс')),
                ('total_sum', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая сумма')),
                ('bank_card', models.CharField(max_length=20, verbose_name='Банковская карта')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создание')),
                ('status', models.PositiveSmallIntegerField(choices=[('Новый', 1), ('В другой стране', 2), ('Отправлен', 3), ('Доставлен', 4)], db_index=True, default=1, verbose_name='Статус')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.products', verbose_name='Товар')),
            ],
        ),
    ]
