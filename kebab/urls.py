from django.contrib import admin
from django.urls import include, path

from kebab import views
from pajtyn_django import settings

urlpatterns = [
    path('kebab/', include('kebab.urls')),
    path('admin/', admin.site.urls),
]
