from django.contrib import admin
from .models import Category, Product, Payment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Payment)