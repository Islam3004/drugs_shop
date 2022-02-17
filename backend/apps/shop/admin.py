from django.contrib import admin

from .models import Products, Categories, SubCategories
# Register your models here.


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "id")


@admin.register(SubCategories)
class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category","id")
    search_fields = ("title", "category__title")
    list_filter = ("category__title",)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "subcategory",
        "price",
        "status",
        "created",
    )
    search_fields = (
        "title",
        "price",
        "category__title",
        "subcategory_title"
    )
    list_filter = (
        "category__title",
        "subcategory__title",
        "status",
        "created",
    )