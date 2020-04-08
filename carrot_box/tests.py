from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from lbworkflow.core.datahelper import load_wf_data

from .wfdata import load_departments
from .wfdata import load_roles
from .wfdata import load_simplewf
from .wfdata import load_users

User = get_user_model()


# create migrations for purchase and do migrate for it.
call_command('makemigrations', 'purchase')
call_command('migrate')


class BaseTests(TestCase):

    def setUp(self):
        self.init_data()

    def init_data(self):
        load_wf_data('lbworkflow')
        self.roles = load_roles()
        self.departments = load_departments()
        self.users = load_users(self.departments, self.roles)
        load_simplewf()


class CarrotTests(BaseTests):

    def test_data(self):
        pass


class PurchaseTests(BaseTests):
    def init_data(self):
        super().init_data()
        load_wf_data('carrot_box.wfapp.purchase')

    def test_data(self):
        pass
