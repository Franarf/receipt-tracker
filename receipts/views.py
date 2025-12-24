from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Min, Max
from django.core.paginator import Paginator

from .forms import ReceiptUploadForm
from .models import Receipt, Vendor


# Create your views here.

def index(request):
    receipts = Receipt.objects.all().order_by("-date")
    vendors = Vendor.objects.all()
    print("Receipts list--------: ",receipts)

    date_range = Receipt.objects.aggregate( 
        earliest=Min("date"), 
        latest=Max("date") 
    )
    
    # Read GET parameters
    query = request.GET.get("q")
    vendor_id = request.GET.get("vendor")
    start_date = request.GET.get("start")
    end_date = request.GET.get("end")
    sort = request.GET.get("sort", "date_desc")
    # get the date range for flatpicker
    date_range = request.GET.get("date_range") 
    start_date = None 
    end_date = None

    if date_range and " - " in date_range: 
        start_date, end_date = date_range.split(" - ")


# Active FILTER dictionary
    active_filters = {}

    # Apply filters
    if query:
        receipts = receipts.filter(
            vendor__name__icontains=query
        ) | receipts.filter(
            ocr_text__icontains=query
        )
        active_filters["q"] = query

    if vendor_id and vendor_id != "all":
        vendor_obj = Vendor.objects.get(id=vendor_id)
        receipts = receipts.filter(vendor=vendor_obj)
       # active_filters["vendor"] = vendor_obj.name

    if start_date:
        receipts = receipts.filter(date__isnull=False, date__gte=start_date)
       # active_filters["start"] = start_date

    if end_date:
        receipts = receipts.filter(date__isnull=False, date__lte=end_date)
       # active_filters["end"] = end_date


 #  SORTING logic
    sort_options = {
        "date_desc": "-date",
        "date_asc": "date",
        "total_desc": "-total",
        "total_asc": "total",
        "vendor_asc": "vendor__name",
        "vendor_desc": "-vendor__name",
    }

    receipts = receipts.order_by(sort_options.get(sort, "-date"))

    # Add sort to active filters (optional)
    active_filters["sort"] = sort

    # Build remove-filter URLs
    remove_urls = {}
    for key in active_filters.keys():
        q = request.GET.copy()
        if key in q:
            del q[key]
        remove_urls[key] = q.urlencode()

    return render(
        request,
        "receipts_list.html",
        {
            "receipts": receipts,
            "vendors": vendors,
            "query": query,
            "selected_vendor": vendor_id,
            "start_date": start_date,
            "end_date": end_date,
            "active_filters": active_filters,
            "remove_urls": remove_urls,
            #"sort": sort, 
            #"earliest_date": date_range["earliest"],
            #"latest_date": date_range["latest"], 
        },
    )

def remove_param(request, param):
    query = request.GET.copy()
    if param in query:
        del query[param]
    return query.urlencode()
# Pagination 
paginator = Paginator(receipts, 10) # 10 receipts per page 
page_number = request.GET.get("page") 
page_obj = paginator.get_page(page_number)

# UPLOAD A RECEIPT
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

#### This loads a single receipt and its items.
def receipt_detail(request, pk):
    receipt = get_object_or_404(Receipt, pk=pk)
    items = receipt.items.all()
    return render(request, "receipt_detail.html", {"receipt": receipt, "items": items})