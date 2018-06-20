from django import forms
from .models import Kebaby_lokale, Kebaby_dania, Inne_dania


class Kebaby_lokaleForm(forms.ModelForm):
    class Meta:
        model = Kebaby_lokale
        fields = ['name', 'city', 'address', 'photo_ref']

        labels = {'name': "Imie", 'city': 'Miasto', 'address': 'Adres', 'photo_ref': "Link do zdjęcia"}


class Kebaby_daniaForm(forms.ModelForm):
    class Meta:
        model = Kebaby_dania
        fields = ['name', 'meat_type', 'meat', 'sauce_type', 'sauce', 'batter_type', 'batter', 'salds', 'photo_ref']

        labels = {'name': "Nazwa dania", 'meat_type': 'Rodzaj mięsa', 'meat': 'Ocena mięsa',
                  'sauce_type': 'Rodzaj sosu', 'sauce': 'Ocena sosu', 'batter_type': 'Rodzaj ciasta',
                  'batter': 'Ocena ciasta',
                  'salds': 'Ocena warzyw (sałatki)', 'photo_ref': "Link do zdjęcia"}


class Inne_daniaForm(forms.ModelForm):
    class Meta:
        model = Inne_dania
        fields = ['name', 'description', 'overall_rate', 'photo_ref']

        labels = {'name': "Nazwa dania", 'description': 'Opisz to danie!', 'overall_rate': 'Oceń to danie!',
                  'photo_ref': "Link do zdjęcia"}


SORTING_CHOICES = (
    ('meat_avg', 'Najlepsze mięso'),
    ('sauce_avg', 'Najlepszy sos'),
    ('batter_avg', 'Najlepsze ciasto'),
    ('salds_avg', 'Najlepsze sałatki'),
    ('overall_avg', 'Najlepiej ocenione lokale'),
)


class Sorting_form(forms.Form):
    sorting = forms.CharField(label="Sortuj", widget=forms.Select(choices=SORTING_CHOICES))
