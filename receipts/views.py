from django.shortcuts import render, redirect
from .forms import ReceiptUploadForm
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Welcome to the Receipts app!")

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