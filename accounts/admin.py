from django.contrib import admin
from accounts.models import Customer,Product,Order,Tag

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)