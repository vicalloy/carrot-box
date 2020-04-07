from django.db import models

from lbworkflow.models import BaseWFObj
from carrot_box.param.models import Param


class Leave(BaseWFObj):
    start_on = models.DateTimeField('Start on')
    end_on = models.DateTimeField('End on')
    leave_days = models.DecimalField('Leave days', max_digits=5, decimal_places=1)

    actual_start_on = models.DateTimeField('Actual start on')
    actual_end_on = models.DateTimeField('Actual end on')
    actual_leave_days = models.DecimalField(
        'Actual leave days', max_digits=5, decimal_places=1)

    leave_type = models.ForeignKey(
        Param, verbose_name='Leave Type',
        on_delete=models.SET_NULL,
        null=True, blank=False,
        limit_choices_to={'param_type__code': 'leave_type', 'is_active': True}
    )
    reason = models.TextField('Reason')

    class Meta:
        verbose_name = 'Leave'
        ordering = ["-created_on"]
        permissions = (
        )

    def __str__(self):
        return '%s %s days' % (self.created_by, self.leave_days, )

    def init_actual_info(self):
        self.actual_start_on = self.start_on
        self.actual_end_on = self.end_on
        self.actual_leave_days = self.leave_days
