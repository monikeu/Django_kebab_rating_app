from django.contrib import admin

# Register your models here.

from .models import Kebaby_lokale, Kebaby_dania, Inne_dania

admin.site.register(Kebaby_lokale)
admin.site.register(Kebaby_dania)
admin.site.register(Inne_dania)