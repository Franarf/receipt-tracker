from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
# Receipts class, for the individual receipts added 
class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    # upload_date = models.DateField(default=timezone.now)
    currency = models.CharField(max_length=3, default="CHF")  # single country
    total = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="receipts/", blank=True, null=True)
    ocr_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Receipt {self.id} - {self.vendor}"

# Items class, for the individual items added on each receipt 
class Item(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    qty = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.qty})"