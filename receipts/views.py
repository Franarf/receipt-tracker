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
    # print("Receipts list--------: ",receipts)

# Earliest / latest dates for Litepicker
    date_range = Receipt.objects.aggregate( 
        earliest=Min("date"), 
        latest=Max("date") 
    )
    
    # Read GET parameters
    query = request.GET.get("q")
    vendor_id = request.GET.get("vendor")
    sort = request.GET.get("sort", "date_desc")

    # Litepicker date range
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
        # vendor_obj = Vendor.objects.get(id=vendor_id)
        receipts = receipts.filter(vendor=vendor_id)
        active_filters["vendor"] = vendor_id.name

    if start_date:
        receipts = receipts.filter(date__isnull=False, date__gte=start_date)
        active_filters["start"] = start_date

    if end_date:
        receipts = receipts.filter(date__isnull=False, date__lte=end_date)
        active_filters["end"] = end_date

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
    active_filters["sort"] = sort
    
 # PAGINATION 
    paginator = Paginator(receipts, 10) # 10 receipts per page 
    page_number = request.GET.get("page") 
    page_obj = paginator.get_page(page_number)
    # print("PAGE OBJ!!!!",page_obj)

# Clean querystring (remove page) 
    query_without_page = request.GET.copy() 
    if "page" in query_without_page: 
        del query_without_page["page"] 
    clean_querystring = query_without_page.urlencode()

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
            "page_obj": page_obj,
            "vendors": vendors,
            "query": query,
            "selected_vendor": vendor_id,
            "date_range": date_range, 
            #"earliest_date": date_limits["earliest"], 
            #"latest_date": date_limits["latest"],
            "active_filters": active_filters,
            "remove_urls": remove_urls,
            "clean_querystring": clean_querystring,
        },
    )

def remove_param(request, param):
    query = request.GET.copy()
    if param in query:
        del query[param]
    return query.urlencode()


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
    print("Rec detail", receipt)
    return render(request, "receipt_detail.html", {"receipt": receipt, "items": items})
    