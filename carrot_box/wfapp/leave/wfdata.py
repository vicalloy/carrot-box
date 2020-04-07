from lbworkflow.core.datahelper import create_category
from lbworkflow.core.datahelper import create_node
from lbworkflow.core.datahelper import create_process
from lbworkflow.core.datahelper import create_transition

from carrot_box.param.models import create_param_type
from carrot_box.param.models import create_param


def load_data():
    load_params()
    load_leave()


def load_params():
    leave_type = create_param_type('leave_type', name='Leave Type')
    create_param('5f31d065-00cc-0000-beea-641f0a670010',
                 param_type=leave_type, name='Vacation')
    create_param('5f31d065-00cc-0000-beea-641f0a670020',
                 param_type=leave_type, name='Sick')


def load_leave():
    """ load_[wf_code] """
    category = create_category('5f31d065-00cc-0010-beea-641f0a670010', 'HR')
    process = create_process('leave', 'Leave', category=category)

    # Nodes
    create_node('5f31d065-00a0-0010-beea-641f0a670010', process, 'Draft', status='draft')
    create_node('5f31d065-00a0-0010-beea-641f0a670020', process, 'Given up', status='given up')
    create_node('5f31d065-00a0-0010-beea-641f0a670030', process, 'Rejected', status='rejected')
    create_node('5f31d065-00a0-0010-beea-641f0a670040', process, 'Completed', status='completed')

    create_node('5f31d065-00a0-0010-beea-641f0a670050', process,
                'Staff Leader', operators='[o.created_by.leader]')
    create_node('5f31d065-00a0-0010-beea-641f0a670060', process,
                'Department Leader', operators='[o.created_by.get_department().leader]')
    create_node('5f31d065-00a0-0010-beea-641f0a670065', process, 'HR', operators='r[hr]')
    create_node('5f31d065-00a0-0010-beea-641f0a670070', process, 'CEO', operators='[ceo]')

    # Transitions
    create_transition('5f31d065-00e0-0010-beea-641f0a670010', process,
                      'Draft', 'Staff Leader')
    create_transition('5f31d065-00e0-0010-beea-641f0a670020', process,
                      'Staff Leader', 'Department Leader')

    create_transition('5f31d065-00e0-0010-beea-641f0a670030', process,
                      'Department Leader', 'HR',
                      condition='o.leave_days<7  # days<7')
    create_transition('5f31d065-00e0-0010-beea-641f0a670040', process,
                      'Department Leader', 'CEO',
                      condition='o.leave_days>=7  # days>=7')
    create_transition('5f31d065-00e0-0010-beea-641f0a670045', process,
                      'CEO', 'HR')

    create_transition('5f31d065-00e0-0010-beea-641f0a670050', process,
                      'HR', 'Completed',
                      app='Customized URL',
                      app_param='wf_execute_transition {{wf_code}} c')
