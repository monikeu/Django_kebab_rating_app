from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
import statistics as s

# Create your views here.
from django.http import HttpResponse
from django.db.models import Sum, Avg

sorting = {
    'meat': lambda lokal: Kebaby_dania.objects.filter(local_id=lokal['id']).aggregate(Avg('meat'))['meat__avg'],
    'batter': lambda lokal: Kebaby_dania.objects.filter(local_id=lokal['id']).aggregate(Avg('batter'))['batter__avg'],
    'salds': lambda lokal: Kebaby_dania.objects.filter(local_id=lokal['id']).aggregate(Avg('salds'))['salds__avg'],
    'sauce': lambda lokal: Kebaby_dania.objects.filter(local_id=lokal['id']).aggregate(Avg('sauce'))['sauce__avg'],
}

from .forms import Kebaby_lokaleForm, Kebaby_daniaForm, Inne_daniaForm, Sorting_form

from .models import Kebaby_dania, Kebaby_lokale, Inne_dania


def noneToInt(result):
    if result is None:
        return 0
    return result


def index(request):
    return HttpResponse("Lubie kebsy")


def wszytskie_lokale_view(request, lokal_sort):
    # lokale = sorting[lokal_sort]
    lokale = Kebaby_lokale.objects.all().values()

    for lokal in lokale:
        lokal['meat_avg'] = noneToInt(sorting['meat'](lokal))
        lokal['salds_avg'] = noneToInt(sorting['salds'](lokal))
        lokal['batter_avg'] = noneToInt(sorting['batter'](lokal))
        lokal['sauce_avg'] = noneToInt(sorting['sauce'](lokal))
        lokal['overall_avg'] = (lokal['meat_avg'] + lokal['salds_avg'] + lokal['batter_avg'] + lokal['sauce_avg']) / 4

    lokale = reversed(sorted(lokale, key=lambda k: k[lokal_sort]))

    form = None

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Sorting_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.label = lokal_sort

            return redirect('kebaby_lokale', lokal_sort=form.data['sorting'])

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Sorting_form()
        form.label = lokal_sort

    template = loader.get_template('kebab/wszystkie_lokale_template.html')

    context = {
        'form': form,
        'lokale': lokale,
    }

    return HttpResponse(template.render(context, request))


def kebab_lokal_view(request, kebaby_lokale_id):
    response = "Tu lokal kebsik numer %s. Będzie lista kebsków i dań z ocenami"

    lokal = Kebaby_lokale.objects.get(id=kebaby_lokale_id)

    dania = Inne_dania.objects.filter(local_id=kebaby_lokale_id)

    kebaby = Kebaby_dania.objects.filter(local_id=kebaby_lokale_id)

    template = loader.get_template('kebab/lokal_templatel.html')

    context = {
        'lokal': lokal,
        'dania': dania,
        'kebaby': kebaby,
        'lokal_id': kebaby_lokale_id
    }

    return HttpResponse(template.render(context, request))


def lokal_new(request):
    template = loader.get_template('kebab/lokal_new_template.html')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Kebaby_lokaleForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_lokal = form.save(commit=False)
            new_lokal.rate = 0
            new_lokal.save()
            return redirect('kebaby_lokale')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Kebaby_lokaleForm()

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def kebab_new(request, kebaby_lokale_id):
    template = loader.get_template('kebab/lokal_new_template.html')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Kebaby_daniaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_danie = form.save(commit=False)
            new_danie.avg_rate = (new_danie.meat + new_danie.sauce + new_danie.batter + new_danie.salds) / 4

            lokal = Kebaby_lokale.objects.get(pk=kebaby_lokale_id)
            new_danie.local_id = lokal
            new_danie.save()
            return redirect('kebaby_lokale')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Kebaby_daniaForm()

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def danie_new(request, kebaby_lokale_id):
    template = loader.get_template('kebab/lokal_new_template.html')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Inne_daniaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            new_danie = form.save(commit=False)
            lokal = Kebaby_lokale.objects.get(pk=kebaby_lokale_id)
            new_danie.local_id = lokal
            new_danie.save()
            return redirect('kebaby_lokale')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = Inne_daniaForm()

    context = {
        'form': form,
    }

    return HttpResponse(template.render(context, request))


def danie_view(request, inne_dania_id):
    response = "Tu danie numer %s."
    return HttpResponse(response % inne_dania_id)


def kebab_danie_view(request, kebaby_dania_id):
    # template = loader.get_template('kebab/kebab_view_template.html')

    response = "Tu kebsik numer %s."
    return HttpResponse(response % kebaby_dania_id)
