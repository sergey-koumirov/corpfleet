from django.shortcuts import render
from django.http import Http404
from .models import War


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


def war_create(request):
    try:
        raw_data = RawData.objects.get(pk=raw_data_id)
    except RawData.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'cta/show.html', {'raw_data': raw_data})