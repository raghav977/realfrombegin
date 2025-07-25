# tenant/middleware.py

from school.models import School
from django.conf import settings
import threading
import os
from django.db import connections
# from db_router import set_current_db_name
# from copy import deepcopy
count =0
BASE_DIR = settings.BASE_DIR 
_thread_locals = threading.local()

from django.conf import settings
from django.db import connections

def add_tenant_db(db_name):
    if db_name not in connections.databases:
        # copy default db config
        new_db_config = settings.DATABASES['default'].copy()
        # override DB name or other keys
        new_db_config['NAME'] = f'{db_name}'
        connections.databases[db_name] = new_db_config
        print("the databases",connections.databases)


def set_current_db_name(db_name):
    
    _thread_locals.db = db_name
    print("This is thread_locals",_thread_locals)
def get_current_db_name():
    print("the current db_name is",getattr(_thread_locals,'db','none'))
    return getattr(_thread_locals, 'db', 'default')

class DbMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/accounts/login/" or request.path == '/create/school/':
            set_current_db_name('default')
            return self.get_response(request)

        # 1. Try query param (for local/dev)
        
        school_code = request.get_host().split('.')[0]
        print("School code used for DB routing:", school_code)

        try:
            tenant = School.objects.using('default').get(school_code=school_code)
            print("Schooled",tenant)
            add_tenant_db(tenant.school_code)
            set_current_db_name(tenant.school_code)
        except School.DoesNotExist:
            set_current_db_name('default')

        return self.get_response(request)
# from django.core.management import call_command

# def run_migrations_for_new_db(db_name):
#     print("Etaa?",db_name)
#     print(f"Running migrate for DB: {db_name}")
#     call_command('migrate', database=db_name, interactive=False, verbosity=2)
