from django.contrib import admin
from django.contrib.auth import get_user_model
from library.models import Order

User = get_user_model()

class OrderInline(admin.TabularInline):
    model = Order
    fields = ['book', 'returnDate']

class UserAdmin(admin.ModelAdmin):
    list_display = ['group', 'last_name']
    list_filter = ['group','username', 'last_name', 'email']
    fields = [('group', 'phone', 'username', 'last_name', 'email', 'password')]
    inlines = [OrderInline]

admin.site.register(User, UserAdmin)