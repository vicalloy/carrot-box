from django.contrib.auth import get_user_model

from carrot_box.tests import BaseTests

from .backends import CarrotModelBackend
from .userparser import CarrotBoxUserParser

User = get_user_model()


class UserSimpleParserTests(BaseTests):

    def test_parser_role(self):
        role_it = self.roles['it']
        users = CarrotBoxUserParser(f"r[{role_it.pk}:it]").parse()
        self.assertEqual(users[0], self.users['it'])

        users = CarrotBoxUserParser(f"r[it]").parse()
        self.assertEqual(users[0], self.users['it'])

    def test_dept_direct_leaders(self):
        users = CarrotBoxUserParser("dept_direct_leaders d[it]").parse()
        self.assertEqual(users[0], self.users['it_dept_leader'])


class PermissionTests(BaseTests):
    def test_get_all_permissions(self):
        backend = CarrotModelBackend()
        it = self.users['it']
        backend.get_all_permissions(it)
