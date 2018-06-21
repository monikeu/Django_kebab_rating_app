from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from .forms import Kebaby_lokaleForm, Kebaby_daniaForm, Sorting_form, UserForm, Kebaby_dania_ocenyForm, LoginForm
from .models import Kebaby_dania, Kebaby_lokale, Kebaby_dania_oceny


def calculate_avg(sorting, lokal):
    dishes = Kebaby_dania.objects.filter(local_id=lokal['id'])

    avg = 0
    for dish in dishes:
        dish_id = dish.id
        avg_ = Kebaby_dania_oceny.objects.filter(danie_id=dish_id).aggregate(Avg(sorting))[sorting + "__avg"]
        avg += noneToInt(avg_)

    avg = avg / (len(dishes) if len(dishes) > 0 else 1)

    return avg


sorting = {
    'meat': lambda lokal: calculate_avg('meat', lokal),
    'batter': lambda lokal: calculate_avg('batter', lokal),
    'salds': lambda lokal: calculate_avg('salds', lokal),
    'sauce': lambda lokal: calculate_avg('sauce', lokal),
}


def noneToInt(result):
    if result is None:
        return 0
    return round(result, 1)


def index(request):
    return HttpResponse("Lubie kebsy")


@login_required
def wszytskie_lokale_view(request, lokal_sort):
    lokale = Kebaby_lokale.objects.all().values()

    for lokal in lokale:
        lokal['meat_avg'] = noneToInt(sorting['meat'](lokal))
        lokal['salds_avg'] = noneToInt(sorting['salds'](lokal))
        lokal['batter_avg'] = noneToInt(sorting['batter'](lokal))
        lokal['sauce_avg'] = noneToInt(sorting['sauce'](lokal))
        lokal['overall_avg'] = round(
            (lokal['meat_avg'] + lokal['salds_avg'] + lokal['batter_avg'] + lokal['sauce_avg']) / 4, 1)

    lokale = reversed(sorted(lokale, key=lambda k: k[lokal_sort + '_avg']))

    form = None

    if request.method == 'POST':
        form = Sorting_form(request.POST)
        if form.is_valid():
            form.label = lokal_sort

            return redirect('kebaby_lokale', lokal_sort=form.data['sorting'])

    else:
        form = Sorting_form()
        form.label = lokal_sort

    template = loader.get_template('kebab/wszystkie_lokale_template.html')

    context = {
        'form': form,
        'lokale': lokale,
    }

    return HttpResponse(template.render(context, request))


@login_required
def kebab_lokal_view(request, kebaby_lokale_id):
    lokal = Kebaby_lokale.objects.get(id=kebaby_lokale_id)

    kebaby = Kebaby_dania.objects.filter(local_id=kebaby_lokale_id).values()

    template = loader.get_template('kebab/lokal_templatel.html')

    for kebab in kebaby:
        avg_meat = 0
        avg_sauce = 0
        avg_salds = 0
        avg_batter = 0
        avg_overall = 0
        oceny = Kebaby_dania_oceny.objects.filter(danie_id=kebab['id']).values()

        for ocena in oceny:
            avg_meat += ocena['meat']
            avg_sauce += ocena['sauce']
            avg_salds += ocena['salds']
            avg_batter += ocena['batter']
            avg_overall += (avg_meat + avg_sauce + avg_salds + avg_batter) / 4

        length = len(oceny) if len(oceny) > 0 else 1
        avg_meat /= length
        avg_sauce /= length
        avg_salds /= length
        avg_batter /= length
        avg_overall /= length

        kebab['avg_meat'] = round(avg_meat, 1)
        kebab['avg_sauce'] = round(avg_sauce, 1)
        kebab['avg_salds'] = round(avg_salds, 1)
        kebab['avg_batter'] = round(avg_batter, 1)
        kebab['avg_overall'] = round(avg_overall, 1)

    context = {
        'lokal': lokal,
        'kebaby': kebaby,
        'lokal_id': kebaby_lokale_id
    }

    return HttpResponse(template.render(context, request))


@login_required
def lokal_new(request):
    template = loader.get_template('kebab/lokal_new_template.html')

    if request.method == 'POST':
        form = Kebaby_lokaleForm(request.POST)
        if form.is_valid():
            new_lokal = form.save(commit=False)
            new_lokal.rate = 0
            new_lokal.save()
            return redirect('kebaby_lokale', lokal_sort='overall')

    else:
        form = Kebaby_lokaleForm()

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required
def kebab_new(request, kebaby_lokale_id):
    template = loader.get_template('kebab/kebab_new_template.html')

    if request.method == 'POST':
        form = Kebaby_daniaForm(request.POST)
        if form.is_valid():
            new_danie = form.save(commit=False)

            lokal = Kebaby_lokale.objects.get(pk=kebaby_lokale_id)
            new_danie.local_id = lokal
            new_danie.save()
            return redirect('kebab_lokal_view', kebaby_lokale_id=kebaby_lokale_id)

    else:
        form = Kebaby_daniaForm()

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required
def kebab_rate_view(request, kebaby_lokale_id, danie_id):
    template = loader.get_template('kebab/kebab_rate_template.html')

    if request.method == 'POST':
        form = Kebaby_dania_ocenyForm(request.POST)
        if form.is_valid():
            new_rate = form.save(commit=False)
            danie = Kebaby_dania.objects.get(pk=danie_id)
            new_rate.danie_id = danie
            new_rate.raterId = request.user.id
            new_rate.save()
            return redirect('kebab_danie_view', kebaby_lokale_id=kebaby_lokale_id, kebaby_dania_id=danie_id)

    else:
        form = Kebaby_dania_ocenyForm()

    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def kebab_view(request, kebaby_lokale_id, kebaby_dania_id):
    template = loader.get_template('kebab/kebab_view_template.html')
    rates = Kebaby_dania_oceny.objects.filter(danie_id=kebaby_dania_id).values()
    kebab = Kebaby_dania.objects.filter(id=kebaby_dania_id).values()[0]

    avg_meat = 0
    avg_sauce = 0
    avg_salds = 0
    avg_batter = 0
    avg_overall = 0
    rater = ''
    for rate in rates:
        avg_meat += rate['meat']
        avg_sauce += rate['sauce']
        avg_salds += rate['salds']
        avg_batter += rate['batter']
        avg_overall += (avg_meat + avg_sauce + avg_salds + avg_batter) / 4
        rater = User.objects.filter(id=rate['raterId']).values()[0]

    length = len(rates) if len(rates) > 0 else 1
    avg_meat /= length
    avg_sauce /= length
    avg_salds /= length
    avg_batter /= length
    avg_overall /= length

    context = {
        'avg_meat': round(avg_meat, 1),
        'avg_sauce': round(avg_sauce, 1),
        'avg_salds': round(avg_salds, 1),
        'avg_batter': round(avg_batter, 1),
        'avg_overall': round(avg_overall, 1),
        'rates': rates,
        'rater': rater,
        'kebab': kebab
    }

    return HttpResponse(template.render(context, request))


def register_view(request):
    template = loader.get_template('kebab/register_template.html')
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            # zwraca user onbejct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('kebaby_lokale', lokal_sort="overall")

        context = {
            'form': form,
            'info': 'Podane dane mają niepoprawną formę, spróbuj jeszcze raz'
        }
        return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm(None)
        context = {
            'form': form,
            'info': 'Utwórz konto'
        }
        return HttpResponse(template.render(context, request))


@login_required
def logout_view(request):
    logout(request)
    return redirect('start_page')


def start_page(request):
    template = loader.get_template('kebab/start_page_template.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # zwraca user onbejct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('kebaby_lokale', lokal_sort="overall")

        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return HttpResponse(template.render(context, request))
