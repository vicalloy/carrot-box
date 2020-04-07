from lbworkflow.core.datahelper import create_user
from lbworkflow.core.datahelper import get_or_create
from lbworkflow.core.datahelper import create_category
from lbworkflow.core.datahelper import create_node
from lbworkflow.core.datahelper import create_process
from lbworkflow.core.datahelper import create_transition

from carrot_box.hr.models import CarrotDepartment
from carrot_box.hr.models import CarrotRole


def load_data():
    roles = load_roles()
    departments = load_departments()
    load_users(departments, roles)
    load_simplewf()


def create_department(*args, **kwargs):
    return get_or_create(CarrotDepartment, *args, **kwargs)


def load_departments():
    root = create_department('f1864b0e-da03-4900-9a3b-54362f611cf5', code='root', name='root', )
    hr = create_department('f1864b0e-da03-4901-9a3b-54362f611cf5', code='hr', name='hr', parent=root, )
    it = create_department('f1864b0e-da03-4902-9a3b-54362f611cf5', code='it', name='it', parent=root, )
    departments = {
        'root': root,
        'hr': hr,
        'it': it,
    }
    return departments


def create_role(*args, **kwargs):
    return get_or_create(CarrotRole, *args, **kwargs)


def load_roles():
    it = create_role('f1864b0e-da02-4900-9a3b-54362f611cf5', code='it', name='it', )
    hr = create_role('f1864b0e-da02-4901-9a3b-54362f611cf5', code='hr', name='hr', )
    roles = {
        'it': it,
        'hr': hr,
    }
    return roles


def load_users(departments, roles):
    ceo = create_user('ceo', department_id=departments['root'].pk)
    departments['root'].leader = ceo
    departments['root'].save()

    tom_leader = create_user('tom_leader', department_id=departments['it'].pk, leader=ceo)
    tom = create_user('tom', department_id=departments['it'].pk, leader=tom_leader)

    it_dept_leader = create_user('it_dept_leader', department_id=departments['it'].pk, leader=ceo)
    it_leader = create_user('it_leader', department_id=departments['it'].pk, leader=it_dept_leader)
    it = create_user('it', department_id=departments['it'].pk, leader=it_leader)
    departments['it'].leader = it_dept_leader
    departments['it'].save()

    hr_dept_leader = create_user('hr_dept_leader', department_id=departments['hr'].pk, leader=ceo)
    hr_leader = create_user('hr_leader', department_id=departments['hr'].pk, leader=hr_dept_leader)
    hr = create_user('hr', department_id=departments['hr'].pk, leader=hr_leader)
    departments['hr'].leader = hr_dept_leader
    departments['hr'].save()

    users = {
        'tom': tom,
        'tom_leader': tom_leader,
        'it': it,
        'it_leader': it_leader,
        'it_dept_leader': it_dept_leader,
        'hr': hr,
        'hr_leader': hr_leader,
        'hr_dept_leader': hr_dept_leader,
        'ceo': ceo,
        'admin': create_user('admin', department_id=departments['root'].pk,
                             leader=ceo, is_superuser=True, is_staff=True),
    }

    roles['it'].users.add(it)
    roles['hr'].users.add(hr, hr_leader, hr_dept_leader)
    return users


def load_simplewf():
    category = create_category('5f31d065-00cc-0020-be00-641f0a670010', 'IT')

    ext_data_buy_computer = {
        'template': """Brand:
Price:
Other requirements:
"""
    }
    process = create_process('simplewf__buy_computer', 'Buy computer',
                             category=category, ext_data=ext_data_buy_computer)
    # Nodes
    create_node('5f31d065-00a0-0010-be00-641f0a670010', process, 'Draft', status='draft')
    create_node('5f31d065-00a0-0010-be00-641f0a670020', process, 'Given up', status='given up')
    create_node('5f31d065-00a0-0010-be00-641f0a670030', process, 'Rejected', status='rejected')
    create_node('5f31d065-00a0-0010-be00-641f0a670040', process, 'Completed', status='completed')
    create_node('5f31d065-00a0-0010-be00-641f0a670060', process,
                'Department Leader', operators='[o.created_by.get_department().leader]')
    create_node('5f31d065-00a0-0010-be00-641f0a670065', process, 'IT', operators='[it]')

    create_transition('5f31d667-0010-0020-be00-641f0a670010', process, 'Draft,', 'Department Leader')
    create_transition('5f31d667-0010-0020-be00-641f0a670020', process, 'Department Leader', 'IT')
    create_transition('5f31d667-0010-0020-be00-641f0a670030', process, 'IT,', 'Completed')

    ext_data_issue = {
        'template': """From:
Requirements:"""
    }
    process = create_process('simplewf__issue', 'Issue', category=category, ext_data=ext_data_issue)
    create_node('5f31d667-00a0-0020-be00-641f0a670010', process, 'Draft', status='draft')
    create_node('5f31d667-00a0-0020-be00-641f0a670020', process, 'Given up', status='given up')
    create_node('5f31d667-00a0-0020-be00-641f0a670030', process, 'Rejected', status='rejected')
    create_node('5f31d667-00a0-0020-be00-641f0a670040', process, 'Completed', status='completed')
    create_node('5f31d065-00a0-0020-be00-641f0a670060', process,
                'IT Leader', operators='dept_direct_leaders d[it]')
    create_node('5f31d065-00a0-0020-be00-641f0a670070', process, 'IT', operators='[it]')

    create_transition('5f31d667-0020-0020-be00-641f0a670010', process, 'Draft,', 'IT Leader')
    create_transition('5f31d667-0020-0020-be00-641f0a670020', process, 'IT Leader', 'IT')
    create_transition('5f31d667-0020-0020-be00-641f0a670030', process, 'IT,', 'Completed')
