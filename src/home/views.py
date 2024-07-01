from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisits
from django.contrib.auth.decorators import login_required


def home_page_view(request, *args, **kwargs):
    PageVisits.objects.create()
    path = request.path
    print("path", path)
    queryset = PageVisits.objects.filter()
    context = {
        "page_visit_count":queryset.count()
    }
    return render(request, "home.html", context)

VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed    
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})