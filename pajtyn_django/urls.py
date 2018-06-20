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

urlpatterns = [
    path('', views.index, name='index'),
    path('start_page/', views.start_page, name='start_page'),
    path('new_account/', views.user_form_view, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
    path('admin/', admin.site.urls),
    path('kebaby_lokale/sort/<lokal_sort>/', views.wszytskie_lokale_view, name='kebaby_lokale'),
    path('kebaby_lokale/<int:kebaby_lokale_id>/', views.kebab_lokal_view, name='kebab_lokal_view'),
    path('kebaby_lokale/<int:kebaby_lokale_id>/kebab/<int:kebaby_dania_id>/', views.kebab_danie_view, name='kebab_danie_view'),
    path('kebaby_lokale/<int:kebaby_lokale_id>/kebab/<danie_id>/rate/', views.kebab_rate_view, name='kebab_rate_view'),
    path('kebaby_lokale/new/', views.lokal_new, name='lokal_new'),
    path('kebaby_lokale/<int:kebaby_lokale_id>/kebab/new/', views.kebab_new, name='kebab_new'),

]
