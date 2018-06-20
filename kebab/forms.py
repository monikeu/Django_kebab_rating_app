from django import forms
from .models import Kebaby_lokale, Kebaby_dania, Kebaby_dania_oceny
from django.contrib.auth.models import User


class Kebaby_lokaleForm(forms.ModelForm):
    class Meta:
        model = Kebaby_lokale
        fields = ['name', 'city', 'address', 'photo_ref']

        labels = {'name': "Nazwa", 'city': 'Miasto', 'address': 'Adres', 'photo_ref': "Link do zdjęcia"}


class Kebaby_daniaForm(forms.ModelForm):
    class Meta:
        model = Kebaby_dania
        fields = ['name', 'meat_type', 'sauce_type', 'batter_type', 'photo_ref']

        labels = {'name': "Nazwa dania", 'meat_type': 'Rodzaj mięsa',
                  'sauce_type': 'Rodzaj sosu', 'batter_type': 'Rodzaj ciasta',
                  'photo_ref': "Link do zdjęcia"}


class Kebaby_dania_ocenyForm(forms.ModelForm):
    class Meta:
        model = Kebaby_dania_oceny
        fields = ['meat', 'sauce', 'batter', 'salds']

        labels = {'name': "Nazwa dania", 'meat': 'Ocena mięsa',
                  'sauce': 'Ocena sosu',
                  'batter': 'Ocena ciasta',
                  'salds': 'Ocena warzyw (sałatki)', 'photo_ref': "Link do zdjęcia"}


SORTING_CHOICES = (
    ('meat', 'Najlepsze mięso'),
    ('sauce', 'Najlepszy sos'),
    ('batter', 'Najlepsze ciasto'),
    ('salds', 'Najlepsze sałatki'),
    ('overall', 'Najlepiej ocenione lokale'),
)


class Sorting_form(forms.Form):
    sorting = forms.CharField(label="Sortuj", widget=forms.Select(choices=SORTING_CHOICES))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(widget=forms.PasswordInput)
