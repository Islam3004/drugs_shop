from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField("Название", max_length = 50, unique=True)
    slug = models.SlugField(max_length = 50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField("Название", max_length = 50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегория"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(verbose_name="Название", max_length=200)
    description = models.TextField(verbose_name="Название")
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Фото", upload_to="products/images/")
    is_active = models.BooleanField("Активный", default=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

