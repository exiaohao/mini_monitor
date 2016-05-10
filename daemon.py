from mongo_utils import monogo_db
import importlib

available_mods = ['fetch_page', ]

mods_kwargs_mapping = {
    'fetch_page': ('connect_timeout', 'read_timeout', 'available_status', 'alert_mail',)
}

if __name__ == '__main__':
    mongo = monogo_db()
    works = mongo.works.find({'work_type': 'fetch_page'})
    for work in works:
        if work['work_type'] in available_mods:
            kwargs = {}
            module_path = "methods.{}".format(work['work_type'])
            module = importlib.import_module(module_path)

            kwargs = {kwarg: work[kwarg] if kwarg in work.keys() else 0 for kwarg in mods_kwargs_mapping[work['work_type']]}
            getattr(module, 'Do')(work['url'], **kwargs)
