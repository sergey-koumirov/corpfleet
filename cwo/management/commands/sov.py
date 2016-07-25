from django.core.management.base import BaseCommand, CommandError
from preston.crest import Preston
import pprint

class Command(BaseCommand):
    help = 'Update Sov Info'

    def handle(self, *args, **options):
        preston = Preston()
        structures = preston.sovereignty.structures()

        print('Pages: {}'.format(structures.pageCount))
        print('Total: {}'.format(structures.totalCount))
        print('Total: {}'.format(len(structures.items)))

        for structure in structures.items:
            if structure.solarSystem.name == 'BWF-ZZ':
                print(structure)

                # bwf = system()
                # pprint.pprint(bwf.data)
                #
                # stats = bwf.stats()
                # pprint.pprint(stats.data)

