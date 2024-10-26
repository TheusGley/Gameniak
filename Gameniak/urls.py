
from django.contrib import admin
from django.urls import path, include
from bond import urls

urlpatterns = [
    path('4dm1n/', admin.site.urls),
    path('',include(urls)),
    
]
