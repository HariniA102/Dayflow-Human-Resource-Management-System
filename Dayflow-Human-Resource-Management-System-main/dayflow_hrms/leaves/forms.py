from django import forms

from accounts.mixins import BootstrapFormMixin

from .models import LeaveRequest


class LeaveRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'remarks']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Reason for leave (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError('End date cannot be earlier than start date.')
        return cleaned_data


class LeaveReviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'admin_comment']
        widgets = {
            'admin_comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Comment (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            (LeaveRequest.Status.APPROVED, 'Approve'),
            (LeaveRequest.Status.REJECTED, 'Reject'),
        ]
