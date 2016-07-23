from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update Sov Info'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):
        for id in options['id']:
            self.stdout.write(self.style.SUCCESS('ID: "%s"' % id))
