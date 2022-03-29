from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Products, Categories, RatingStar, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.

class ProductsAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    detail = forms.CharField(label='Детали', widget=CKEditorUploadingWidget())

    class Meta:
        model = Products
        fields = '__all__'




admin.site.register(RatingStar)
class ReviewsAdminForm(forms.ModelForm):
    text = forms.CharField(label="Комментарий", widget=CKEditorUploadingWidget())

    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_image', 'price', 'discount', 'status', 'created')
    list_filter = ('category', 'created', 'status')
    search_fields = ('title', 'category__title', 'price')
    list_editable = ('status',)
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category',)
    save_on_top = True
    inlines = (ReviewInline,)
    form = ProductsAdminForm

    fieldsets = (
        ("Название, категория и фото товара", {
            "fields": (('title', 'slug'), 'image', 'category')
        }),

        ("Описание", {
            "fields": ('description', 'detail')
        }),

        ("Количество товара, скидка и цена", {
            "fields": (('price', 'discount'), 'status', 'favorites')
        }),
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='40' height='50'")

    get_image.short_description = 'Изображение'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created')
    search_fields = ('id', 'user__first_name', 'product__title', 'user__last_name', 'user__email')
    list_display_links = ('product', 'user')
    list_filter = ('user__first_name', 'product')
    form = ReviewsAdminForm


admin.site.site_title = "Drugs Shop"
admin.site.site_header = "Drugs Shop"

