from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from lbutils import get_or_none

from carrot_box.param.models import Param
from carrot_box.tests import BaseTests

from .models import Leave
from .wfdata import load_data

User = get_user_model()


class LeaveTests(BaseTests):

    def setUp(self):
        super().setUp()
        self.client.login(username='tom', password='password')
        self.leave_type_vacation = Param.objects.get(param_type__code='leave_type', name='Vacation')
        self.leave = self.create_leave('reason', False)

    def init_data(self):
        super().init_data()
        load_data()

    def create_leave(self, reason, submit=True):
        leave = Leave(
            start_on=timezone.now(), end_on=timezone.now(), leave_days=1,
            leave_type=self.leave_type_vacation,
            reason=reason, created_by=self.users['tom'])
        leave.init_actual_info()
        leave.save()
        leave.create_pinstance('leave', submit)
        return leave

    def get_leave(self, reason):
        return get_or_none(Leave, reason=reason)

    def test_list(self):
        resp = self.client.get(reverse('wf_list', args=('leave', )))
        self.assertEqual(resp.status_code, 200)

    def test_export(self):
        resp = self.client.get(reverse('wf_list', args=('leave', )), {'export': 1})
        self.assertEqual(resp.status_code, 200)

    def test_detail(self):
        resp = self.client.get(reverse('wf_detail', args=(self.leave.pinstance.pk, )))
        self.assertEqual(resp.status_code, 200)

    def test_submit(self):
        self.client.login(username='tom', password='password')

        url = reverse('wf_new', args=('leave', ))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = {
            'start_on': '2017-04-19 09:01',
            'end_on': '2017-04-20 09:01',
            'leave_type': self.leave_type_vacation.pk,
            'leave_days': '1',
            'reason': 'test save',
        }
        resp = self.client.post(url, data)
        leave = Leave.objects.get(reason='test save')
        self.assertRedirects(resp, '/wf/%s/' % leave.pinstance.pk)
        self.assertEqual('Draft', leave.pinstance.cur_node.name)

        data['act_submit'] = 'Submit'
        data['reason'] = 'test submit'
        resp = self.client.post(url, data)
        leave = Leave.objects.get(reason='test submit')
        self.assertRedirects(resp, '/wf/%s/' % leave.pinstance.pk)
        self.assertEqual('Staff Leader', leave.pinstance.cur_node.name)

    def test_edit(self):
        self.client.login(username='tom', password='password')

        data = {
            'start_on': '2017-04-19 09:01',
            'end_on': '2017-04-20 09:01',
            'leave_type': self.leave_type_vacation.pk,
            'leave_days': '1',
            'reason': 'test save',
        }
        url = reverse('wf_new', args=('leave', ))
        resp = self.client.post(url, data)
        leave = Leave.objects.get(reason='test save')
        self.assertRedirects(resp, '/wf/%s/' % leave.pinstance.pk)
        self.assertEqual('Draft', leave.pinstance.cur_node.name)

        url = reverse('wf_edit', args=(leave.pinstance.pk, ))
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data['act_submit'] = 'Submit'
        data['reason'] = 'test submit'
        resp = self.client.post(url, data)
        leave = Leave.objects.get(reason='test submit')
        self.assertRedirects(resp, '/wf/%s/' % leave.pinstance.pk)
        self.assertEqual('Staff Leader', leave.pinstance.cur_node.name)

    def test_delete(self):
        self.client.login(username='admin', password='password')
        # POST
        url = reverse('wf_delete')
        leave = self.create_leave('to delete')
        data = {'pk': leave.pinstance.pk}
        resp = self.client.post(url, data)
        self.assertRedirects(resp, '/wf/list/')
        self.assertIsNone(self.get_leave('to delete'))

        # GET
        leave = self.create_leave('to delete')
        data = {'pk': leave.pinstance.pk}
        resp = self.client.get(url, data)
        self.assertRedirects(resp, '/wf/list/')
        self.assertIsNone(self.get_leave('to delete'))
