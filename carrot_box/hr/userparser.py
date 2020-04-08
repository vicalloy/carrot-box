from django.contrib.auth import get_user_model
from lbworkflow.core.userparser import SimpleUserParser

from .models import CarrotDepartment
from .models import CarrotRole

User = get_user_model()


class CarrotBoxUserParser(SimpleUserParser):
    def process_func(self, func_str):
        """
        return None if not a func
        """
        params = [e.strip() for e in func_str.split(' ') if e.strip()]
        func_name = params[0]
        params = params[1:]
        if not params:  # at least one param
            return None
        elif func_name == 'dept_direct_leaders':
            departments = self.get_departments(params[0])
            return [d.leader for d in departments if d.leader]
        return None  # if not function return None

    def get_departments(self, atom_str):
        """
        d[o.dept]
        d[o.depts]
        d[11:it]
        """
        return self.get_object_list(atom_str, CarrotDepartment, 'code', 'd[')

    def get_roles(self, role_str):
        """
        r[hr]
        r[1:hr]
        """
        return self.get_object_list(role_str, CarrotRole, 'code', 'r[')

    def get_users_by_roles(self, role_str):
        roles = self.get_roles(role_str)
        return User.objects.filter(roles__in=roles)

    def parse_atom_rule(self, atom_rule):
        if atom_rule and atom_rule.startswith('r['):
            return self.get_users_by_roles(atom_rule)
        return super().parse_atom_rule(atom_rule)
