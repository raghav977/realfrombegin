
from school.middleware import get_current_db_name
from django.conf import settings
class TenantDatabaseRouter:
    def db_for_read(self, model, **hints):
        # print("This is app_level?",model._meta.app_label)
        return get_current_db_name()

    def db_for_write(self, model, **hints):
        return get_current_db_name()

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = get_current_db_name()
        db_obj2 = get_current_db_name()
        return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        current_db = get_current_db_name()
        db_name = settings.DATABASES[db]['NAME']  # This gives actual DB name
        print("This is db:", db_name)
        print("This is current_db:", current_db)
        if not db_name=='default':
            current_db=db_name
        print("This is db:", db_name)
        print("This is current_db:", current_db)
        return db_name == current_db
