from django.test import TestCase
from django.contrib.auth.models import User
from .models import Vendor, Receipt, Item
from django.db.models import Sum, Avg
from datetime import date

# Create your tests here.

class ReceiptModelTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username="tester", password="test123")

        # Create vendor
        self.vendor = Vendor.objects.create(name="Coop", address="Bahnhofstrasse 1, Geneve")

        # Create receipt
        self.receipt = Receipt.objects.create(
            user=self.user,
            vendor=self.vendor,
            date=date(2025, 12, 17),
            currency="CHF",
            total=15.50,
            ocr_text="Milk 1L 2.50\nBread 3.00\nCheese 10.00"
        )

        # Create items
        Item.objects.create(receipt=self.receipt, name="Milk 1L", qty=1, unit_price=2.50, line_total=2.50)
        Item.objects.create(receipt=self.receipt, name="Bread", qty=1, unit_price=3.00, line_total=3.00)
        Item.objects.create(receipt=self.receipt, name="Cheese", qty=1, unit_price=10.00, line_total=10.00)

    def test_receipt_total(self):
        """Check that receipt total matches sum of items"""
        total_items = self.receipt.items.aggregate(Sum("line_total"))["line_total__sum"]
        self.assertEqual(float(total_items), float(self.receipt.total))

    def test_vendor_name(self):
        """Check vendor name is stored correctly"""
        self.assertEqual(self.vendor.name, "Coop")

    def test_items_count(self):
        """Check number of items in receipt"""
        self.assertEqual(self.receipt.items.count(), 3)

    def test_average_price_of_milk(self):
        """Check average price query works"""
        avg_price = Item.objects.filter(name__icontains="Milk").aggregate(Avg("unit_price"))["unit_price__avg"]
        self.assertEqual(float(avg_price), 2.50)

    def test_receipts_by_user(self):
        """Check receipts can be filtered by user"""
        receipts = Receipt.objects.filter(user__username="tester")
        self.assertEqual(receipts.count(), 1)

    def test_items_above_price(self):
        """Check items above 5 CHF are returned"""
        expensive_items = Item.objects.filter(unit_price__gt=5.00)
        self.assertEqual(expensive_items.count(), 1)
        self.assertEqual(expensive_items.first().name, "Cheese")

# in future-- create tests based on sampled ites, or existing receipts 