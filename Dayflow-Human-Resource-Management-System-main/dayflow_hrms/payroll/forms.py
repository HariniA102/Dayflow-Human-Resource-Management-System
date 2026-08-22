from django import forms

from accounts.mixins import BootstrapFormMixin

from .models import SalaryStructure


class SalaryStructureForm(BootstrapFormMixin, forms.ModelForm):
    """FR 3.6.2: Admin can update salary structure."""

    class Meta:
        model = SalaryStructure
        fields = [
            'basic', 'hra', 'conveyance_allowance', 'other_allowances',
            'provident_fund', 'tax_deduction', 'other_deductions',
        ]
