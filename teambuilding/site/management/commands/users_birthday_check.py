from django.core.management.base import BaseCommand

from teambuilding.site.tasks import check_users_birthday


class Command(BaseCommand):
    help = "Checks if today is the birthday of a registered user."

    def handle(self, *args, **options):
        check_users_birthday()
        self.stdout.write(self.style.SUCCESS("Birthday check done."))
