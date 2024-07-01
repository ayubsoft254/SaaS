from django.urls import path

from profiles.views import profile_view

urlpatterns = [
    path("<str:username>/", profile_view, name="profiler"),    
]
