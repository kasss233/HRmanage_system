from django.contrib import admin
from .models import Salary, SalaryStandard


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'level','bonus', 'total_salary', 'payment_status')
    search_fields = ('id', 'payment_status')


@admin.register(SalaryStandard)
class SalaryStandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'standard_no', 'standard_name', 'basic_salary', 'standard_status')
    search_fields = ('standard_no', 'standard_name', 'creator', 'registrar')
