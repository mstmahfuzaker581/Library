from django.contrib import admin
from .models import Category, Book, Reviews, BorrowedBook
# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Reviews)
admin.site.register(BorrowedBook)