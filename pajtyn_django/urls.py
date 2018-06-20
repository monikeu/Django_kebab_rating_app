"""pajtyn_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import kebab.views as views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('kebaby_lokale/<lokal_sort>/', views.wszytskie_lokale_view, name='kebaby_lokale'),
    path('<int:kebaby_lokale_id>/', views.kebab_lokal_view, name='results'),
    path('kebaby/<int:kebaby_dania_id>/', views.kebab_danie_view, name='results'),
    path('kebaby_lokale/new/', views.lokal_new, name='lokal_new'),
    path('<int:kebaby_lokale_id>/danie/new/', views.danie_new, name='danie_new'),
    path('<int:kebaby_lokale_id>/kebab/new/', views.kebab_new, name='kebab_new'),

]
