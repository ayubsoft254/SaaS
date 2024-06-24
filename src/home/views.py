from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisits

def home_page_view(request, *args, **kwargs):
    PageVisits.objects.create()
    path = request.path
    print("path", path)
    queryset = PageVisits.objects.filter()
    context = {
        "page_visit_count":queryset.count()
    }
    return render(request, "home.html", context)