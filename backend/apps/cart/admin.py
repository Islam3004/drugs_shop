from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'fio', 'address', 'post_code', 'status','created', 'user']
    list_display_links = ['fio',]
    search_fields = ['fio', 'email', 'id', 'user']
    list_editable = ['status', ]
    list_filter = ['created', 'status',]
    inlines = [OrderItemInline,]