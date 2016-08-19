from django.shortcuts import render
from django.http import Http404
from .models import RawData
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    raw_datas = RawData.objects.order_by('-date').all()
    context = {
        'raw_datas': raw_datas
    }
    return render(request, 'cta/index.html', context)


@login_required
def show(request, raw_data_id):
    try:
        raw_data = RawData.objects.get(pk=raw_data_id)
    except RawData.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'cta/show.html', {'raw_data': raw_data})


@login_required
def update(request, raw_data_id):
    try:
        raw_data = RawData.objects.get(pk=raw_data_id)
    except RawData.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'cta/show.html', {'raw_data': raw_data})
