<<<<<<< HEAD
# Generated by Django 3.2.9 on 2022-03-24 16:46
=======
# Generated by Django 3.2.9 on 2022-03-29 13:32
>>>>>>> d91da954264104d0a8d731c78a2e54493054d42d

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, null=True, unique=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('description', models.TextField(verbose_name='Описание')),
                ('detail', models.TextField(verbose_name='Детали')),
                ('price', models.DecimalField(decimal_places=2, max_digits=100, verbose_name='Цена')),
                ('discount', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Скидка')),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.categories', verbose_name='Категория')),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorites_users', to=settings.AUTH_USER_MODEL, verbose_name='Избранное')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда к рейтингу',
                'verbose_name_plural': 'Звезды к рейтингу',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комметарий')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
                ('star', models.ForeignKey(null=True, on_delete=django.db.models.fields.CharField, to='shop.ratingstar', verbose_name='Звезды')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created'],
            },
        ),
    ]
