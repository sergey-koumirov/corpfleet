from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.http import HttpResponse
from .models import War
from .models import Alliance
from .models import Region
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


def add_participant(request, war_id):
    try:
        json_data = json.loads(request.body.decode("utf-8"))
        war = War.objects.get(pk=war_id)
        war.participant_set.create(name=json_data['name'], color=json_data['color'])
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def delete_participant(request, war_id, participant_id):
    try:
        war = War.objects.get(pk=war_id)
        participant = war.participant_set.get(pk=participant_id)
        participant.delete()
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def add_alliance(request, war_id, participant_id):
    try:
        json_data = json.loads(request.body.decode("utf-8"))
        war = War.objects.get(pk=war_id)
        participant = war.participant_set.get(pk=participant_id)
        alliance = Alliance.objects.get(pk=json_data['id'])
        participant.participantalliance_set.create(
            participant=participant,
            alliance=alliance,
            date1=json_data['date1'],
            date2=json_data['date2']
        )
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def delete_alliance(request, war_id, participant_id, pa_id):
    try:
        war = War.objects.get(pk=war_id)
        participant = war.participant_set.get(pk=participant_id)
        pa = participant.participantalliance_set.get(pk=pa_id)
        pa.delete()
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def update_alliance(request, war_id, participant_id, pa_id):
    try:
        war = War.objects.get(pk=war_id)
        participant = war.participant_set.get(pk=participant_id)
        pa = participant.participantalliance_set.get(pk=pa_id)

        json_data = json.loads(request.body.decode("utf-8"))
        pa.date1 = json_data['date1']
        pa.date2 = json_data['date2']
        pa.save()

        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def add_territory(request, war_id):
    try:
        json_data = json.loads(request.body.decode("utf-8"))
        war = War.objects.get(pk=war_id)
        war.territory_set.create(name=json_data['name'])
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def delete_territory(request, war_id, territory_id):
    try:
        war = War.objects.get(pk=war_id)
        territory = war.territory_set.get(pk=territory_id)
        territory.delete()
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def add_region(request, war_id, territory_id):
    try:
        json_data = json.loads(request.body.decode("utf-8"))
        war = War.objects.get(pk=war_id)
        territory = war.territory_set.get(pk=territory_id)
        region = Region.objects.get(pk=json_data['id'])
        territory.territoryregion_set.create(territory=territory, region=region)
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def delete_region(request, war_id, territory_id, tr_id):
    try:
        war = War.objects.get(pk=war_id)
        territory = war.territory_set.get(pk=territory_id)
        tr = territory.territoryregion_set.get(pk=tr_id)
        tr.delete()
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def info(request, war_id):
    try:
        war = War.objects.get(pk=war_id)
        return HttpResponse(json.dumps(war.info()), content_type="application/json")
    except War.DoesNotExist:
        raise Http404("War does not exist")


def war_alliances(request):
    q = request.GET.get('term', '')
    alliances = []
    for r in Alliance.objects.filter(name__icontains=q).order_by('name')[:10]:
        alliances.append({'id': r.id, 'name': r.name})
    return HttpResponse(json.dumps(alliances), content_type="application/json")


def war_regions(request):
    q = request.GET.get('term', '')
    regions = []
    for r in Region.objects.filter(name__icontains=q).order_by('name')[:10]:
        regions.append({'id': r.id, 'name': r.name})
    return HttpResponse(json.dumps(regions), content_type="application/json")

def war_dashboard(request, war_id):
    try:
        war = War.objects.get(pk=war_id)
        return render(request, 'cwo/war/dashboard.html', {'war': war, 'border': war.minmax()})
    except War.DoesNotExist:
        raise Http404("War does not exist")