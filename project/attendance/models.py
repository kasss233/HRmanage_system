from django.db import models
from employee.models import employee
<<<<<<< HEAD
from datetime import timedelta
from django.utils import timezone

class Attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    sign_in = models.DateTimeField(null=True)
    sign_out = models.DateTimeField(null=True)
    is_sign_in = models.BooleanField(default=False)
    is_sign_out = models.BooleanField(default=False)
    remarks = models.TextField(null=True)

    is_late = models.BooleanField(default=False)  # 新增字段，保存是否迟到
    is_early = models.BooleanField(default=False)  # 新增字段，保存是否早退
    is_absent = models.BooleanField(default=False)  # 新增字段，保存是否缺勤

    def save(self, *args, **kwargs):
        """ 在保存时计算是否迟到、早退或缺勤，判断当天是否需要执行计算 """

        # 获取今天的日期
        today = timezone.now().date()

        # 如果是当天的数据，不执行迟到、早退和缺勤的计算
        if self.date == today:
            # 如果是当天的记录，跳过计算
            super().save(*args, **kwargs)
            return

        # 如果是当天以后或其他日期的记录，计算迟到、早退和缺勤
        if self.is_sign_in and self.sign_in:
            # 处理签到时间是否迟到
            work_start_time = self.date + timedelta(hours=9)  # 假设9点是规定的上班时间
            if self.sign_in > work_start_time:
                self.is_late = True
            else:
                self.is_late = False

        if self.is_sign_out and self.sign_out:
            # 处理签退时间是否早退
            work_end_time = self.date + timedelta(hours=17)  # 假设17点是规定的下班时间
            if self.sign_out < work_end_time:
                self.is_early = True
            else:
                self.is_early = False

        if not self.is_sign_in:
            self.is_absent = True
        else:
            self.is_absent = False

        # 调用父类的 save 方法保存数据
        super().save(*args, **kwargs)

    @classmethod
    def get_late_count(cls, employee_id):
        """ 获取某个员工的迟到次数，基于 employee_id """
        return cls.objects.filter(employee_id=employee_id, is_late=True).count()

    @classmethod
    def get_early_count(cls, employee_id):
        """ 获取某个员工的早退次数，基于 employee_id """
        return cls.objects.filter(employee_id=employee_id, is_early=True).count()

    @classmethod
    def get_absent_count(cls, employee_id):
        """ 获取某个员工的缺勤次数，基于 employee_id """
        return cls.objects.filter(employee_id=employee_id, is_absent=True).count()
=======
class Attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    date=models.DateField(null=True)
    sign_in=models.DateTimeField(null=True)
    sign_out=models.DateTimeField(null=True)
    is_sign_in=models.BooleanField(default=False)
    is_sign_out=models.BooleanField(default=False)
    remarks=models.TextField(null=True)
>>>>>>> 29db69bdcee67c93b3434565e9ef4f2c3d1b0220
