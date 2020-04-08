from lbworkflow.core.datahelper import create_category
from lbworkflow.core.datahelper import create_node
from lbworkflow.core.datahelper import create_process
from lbworkflow.core.datahelper import create_transition


def load_data():
    load_issue()


def load_issue():
    """ load_[wf_code] """
    category = create_category('5f31d065-00cc-0020-be00-641f0a670010', 'IT')
    process = create_process('purchase', 'Purchase', category=category)
    create_node('5f31d065-00a0-0030-beea-641f0a670010', process, 'Draft', status='draft')
    create_node('5f31d065-00a0-0030-beea-641f0a670020', process, 'Given up', status='given up')
    create_node('5f31d065-00a0-0030-beea-641f0a670030', process, 'Rejected', status='rejected')
    create_node('5f31d065-00a0-0030-beea-641f0a670040', process, 'Completed', status='completed')
    create_node('5f31d065-00a0-0030-beea-641f0a670050', process, 'IT', operators='[it]')
    create_transition('5f31d065-00e0-0030-beea-641f0a670010', process, 'Draft,', 'IT')
    create_transition('5f31d065-00e0-0030-beea-641f0a670020', process, 'IT,', 'Completed')