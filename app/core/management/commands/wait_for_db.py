"""
Django command to wait for the db to be available.
"""
import time

from psycopg2 import OperationalError as Psycorpg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('waiting for DB to start...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycorpg2OpError, OperationalError):
                self.stdout.write(self.style.WARNING(
                    'DB unavailable, waiting 1 second...'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB available!'))
