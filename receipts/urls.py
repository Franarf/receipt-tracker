from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="receipts-index"),
    path("upload/", views.upload_receipt, name="upload-receipt"),
    path("upload/success/", views.upload_success, name="upload-success"),
    path("<int:pk>/", views.receipt_detail, name="receipt-detail"),
]