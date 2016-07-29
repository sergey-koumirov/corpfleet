from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import War
from .models import Alliance
import json

def war_index(request):
    wars = War.objects.order_by('-id').all()
    context = {
        'wars': wars
    }
    return render(request, 'cwo/war/index.html', context)


def war_new(request):
    war = War()
    context = {
        'war': war
    }
    return render(request, 'cwo/war/edit.html', context)


def war_edit(request, war_id):
    try:
        war = War.objects.get(pk=war_id)
    except War.DoesNotExist:
        raise Http404("War does not exist")
    return render(request, 'cwo/war/edit.html', {'war': war})


def war_create(request):
    try:
        raw_data = War.objects.get(pk=1)
    except War.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'cta/show.html', {'raw_data': raw_data})


def war_alliances(request):
    q = request.GET.get('term', '')
    alliances = []
    for r in Alliance.objects.filter(name__icontains=q).order_by('name')[:10]:
        alliances.append({'id': r.id, 'name': r.name})
    return HttpResponse(json.dumps(alliances), content_type="application/json")