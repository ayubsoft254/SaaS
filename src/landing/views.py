import helpers.numbers
from django.shortcuts import render

# Create your views here.
from dashboard.views import dashboard_view

from visits.models import visits_pagevisit

def landing_dashboard_page_view(request):
    if request.user.is_authenticated:
        return dashboard_view(request)  
    
    return render(request, "landing/main.html", {})