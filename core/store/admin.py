from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

# Order-er detail page-e jeno product list dekha jay
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ['product_name', 'price', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    # List page-e ja ja dekhabe
    list_display = ['id', 'user', 'full_name', 'total_price', 'payment_status', 'status', 'created_at']
    
    # List page thekei jeno status change kora jay (Dropdown)
    list_editable = ['status', 'payment_status']
    
    # Side-e filter option
    list_filter = ['status', 'payment_status', 'created_at']
    
    # Search korar sujog
    search_fields = ['full_name', 'phone_number', 'transaction_id']
    
    # Order detail-er bhetore product list dekhabe
    inlines = [OrderItemInline]

# Shob model gulo ekbar kore register koro
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)