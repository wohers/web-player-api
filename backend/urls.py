# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("API is working!")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
]