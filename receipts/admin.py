from django.contrib import admin
from .models import Vendor, Receipt, Item

# Register your models here.

admin.site.register(Vendor)
admin.site.register(Receipt)
admin.site.register(Item)
