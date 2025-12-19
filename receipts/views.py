from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import ReceiptUploadForm
from .models import Receipt


# Create your views here.

def index(request):
    # return HttpResponse("Welcome to the Receipts app!")
    receipts = Receipt.objects.all().order_by("-date")
    return render(request, "receipts_list.html", {"receipts": receipts})

def upload_receipt(request):
    if request.method == "POST":
        form = ReceiptUploadForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user  # temporary until auth is added
            receipt.save()
            return redirect("upload-success")
    else:
        form = ReceiptUploadForm()

    return render(request, "upload.html", {"form": form})


def upload_success(request):
    return render(request, "upload_success.html")