from django.contrib.auth import get_user_model
from carrot_box.tests import BaseTests
from .wfdata import load_leave

User = get_user_model()


class LeaveTests(BaseTests):

    def setUp(self):
        super().setUp()

    def init_data(self):
        super().init_data()
        load_leave()

    def test_data(self):
        pass
