from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
from cwo.models import Region

import pprint

class Command(BaseCommand):
    help = 'Create Map Records'

    def handle(self, *args, **options):
        preston = Preston()
        regions = preston.regions()

        for region in regions.items:
            obj, created = Region.objects.get_or_create(id=region.id, name=region.name)
            obj.save()

