from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from .models import War
from .models import Alliance
from .forms import WarForm
import json
import datetime


def war_index(request):
    wars = War.objects.order_by('-id').all()
    context = {
        'wars': wars
    }
    return render(request, 'cwo/war/index.html', context)


def war_new(request):
    war = War()
    war.name = '[ {0:%Y-%m-%d %H:%M:%S} ] Red vs Blue'.format(datetime.datetime.now())
    context = {
        'war': WarForm(instance=war)
    }
    return render(request, 'cwo/war/new.html', context)


def war_create(request):
    war = WarForm(request.POST)
    if war.is_valid():
        war.save()
        return redirect('cwo:war_edit', war.instance.id)
    else:
        return render(request, 'cwo/war/new.html', {'war': war})


def war_edit(request, war_id):
    try:
        war = War.objects.get(pk=war_id)
    except War.DoesNotExist:
        raise Http404("War does not exist")
    return render(request, 'cwo/war/edit.html', {'war': WarForm(instance=war)})


def war_update(request, war_id):
    try:
        instance = War.objects.get(pk=war_id)
        war = WarForm(request.POST, instance=instance)
        if war.is_valid():
            war.save()
            return redirect('cwo:war_edit', war.instance.id)
        else:
            return render(request, 'cwo/war/edit.html', {'war': war})

    except War.DoesNotExist:
        raise Http404("War does not exist")


def war_delete(request, war_id):
    try:
        instance = War.objects.get(pk=war_id)
        instance.delete()
        return redirect('cwo:war_index')
    except War.DoesNotExist:
        raise Http404("War does not exist")


def add_war_side(request, war_id):
    try:
        instance = War.objects.get(pk=war_id)
        return HttpResponse(json.dumps({'s': 1}), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def war_alliances(request):
    q = request.GET.get('term', '')
    alliances = []
    for r in Alliance.objects.filter(name__icontains=q).order_by('name')[:10]:
        alliances.append({'id': r.id, 'name': r.name})
    return HttpResponse(json.dumps(alliances), content_type="application/json")