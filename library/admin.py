from django.contrib import admin
from .models import Book, Order, Rating, Comment

    
class CommentInline(admin.TabularInline):
    model = Comment

class RatingInline(admin.TabularInline):
    model = Rating

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'book_id', 'is_available']
    list_filter = ['title', "is_available"]
    inlines = [CommentInline, RatingInline]

admin.site.register(Book, BookAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['student','book','is_returned','dateOfIssue', 'returnDate']
    list_filter = ['dateOfIssue', 'returnDate', "is_returned"]

admin.site.register(Order, OrderAdmin)
