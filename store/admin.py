from django.contrib import admin
from . import models


@admin.action(description='ACTIVE')
def set_orders_as_active(modeladmin, request, queryset):
    queryset.update(status='ACTIVE')


@admin.action(description='COMPLETED')
def set_orders_as_complete(modeladmin, request, queryset):
    queryset.update(status='COMPLETED')


@admin.action(description='CANCELED')
def set_orders_as_cancel(modeladmin, request, queryset):
    queryset.update(status='CANCELED')


@admin.action(description='SUSPENDED')
def set_orders_as_suspend(modeladmin, request, queryset):
    queryset.update(status='SUSPENDED')


class OrderItemInline(admin.TabularInline):
    """
    Admin inline for OrderItem model
    """
    model = models.OrderItem
    fields = (
        'product',
        'qty',
        'price',
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        OrderItemInline,
    )
    list_filter = (
        'status',
        'created_on',
    )
    list_display = (
        '__str__',
        'status',
        'created_on',
    )
    list_editable = (
        'status',
    )
    search_fields = (
        'status',
        'owner__id',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )
    list_per_page = 10
    list_max_show_all = 20
    actions = [
        set_orders_as_active,
        set_orders_as_complete,
        set_orders_as_cancel,
        set_orders_as_suspend,
    ]
