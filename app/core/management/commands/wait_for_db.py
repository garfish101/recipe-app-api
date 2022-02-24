import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution untile database is avalable"""
    def handle(self,*args,**options):
        self.stdout.write('Waiting for database ...')
        db_conn =None 
        while not db_conn:
            try:
                db_conn = connections['defualt']
            except OperationalError:
                self.stdout.write('Database unavalable, waiting 1 second ... ')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database avalable'))