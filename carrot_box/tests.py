from django.contrib.auth import get_user_model
from django.test import TestCase
from .wfdata import load_departments
from .wfdata import load_roles
from .wfdata import load_users

from lbworkflow.core.datahelper import load_wf_data

User = get_user_model()


class BaseTests(TestCase):

    def setUp(self):
        self.init_data()

    def init_data(self):
        load_wf_data('lbworkflow')
        self.roles = load_roles()
        self.departments = load_departments()
        self.users = load_users(self.departments, self.roles)

    def test_data(self):
        pass
