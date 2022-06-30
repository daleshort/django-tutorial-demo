

from django.contrib import admin
from . import models
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
# Register your models here.


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_select_related = ['collection']
    list_filter = ['collection']

    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        else:
            return 'ok'

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description='clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were sucessfully updated'
        )


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Customer)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name']
    search_fields = ['first_name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    inlines = [OrderItemInline]
    search_fields = ['id']
    autocomplete_fields = ['customer']
