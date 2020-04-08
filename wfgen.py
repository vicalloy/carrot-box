import os
import uuid
import sys

import django
from django.core.management import call_command
from lbworkflow.flowgen import FlowAppGenerator
from lbworkflow.flowgen import clean_generated_files


def gen():
    from carrot_box.wfapp.purchase.models import Purchase as wf_class
    from carrot_box.wfapp.purchase.models import Item as wf_item_class
    FlowAppGenerator().gen(wf_class, [wf_item_class], replace=True)


def clean():
    from carrot_box.wfapp.purchase.models import Purchase
    clean_generated_files(Purchase)


def load_data():
    from lbworkflow.core.datahelper import load_wf_data
    load_wf_data('carrot_box.wfapp.purchase')


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = "carrot_box.settings"
    django.setup()
    if (len(sys.argv)) == 2:
        cmd = sys.argv[1]
        if cmd == 'clean':
            clean()
        elif cmd == 'uuid':
            print(str(uuid.uuid4()))
        elif cmd == "parse":
            from carrot_box.hr.userparser import CarrotBoxUserParser
            print(CarrotBoxUserParser("dept_direct_leaders d[it]").parse())
        sys.exit(0)
    gen()
    call_command('makemigrations', 'purchase')
    call_command('migrate')
    load_data()
