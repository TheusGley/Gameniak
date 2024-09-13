
from django.contrib import admin
from django.urls import path, include
from bond import urls

urlpatterns = [
    path('4dmin/', admin.site.urls),
    path('',include(urls)),
    
]
