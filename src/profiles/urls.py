from django.urls import path

from profiles.views import profile_detail_view,profile_list_view

urlpatterns = [
    path("<str:username>/", profile_detail_view, name="profile_detail_view"),
    path("", profile_list_view, name="profiler_list_view"),    
]
