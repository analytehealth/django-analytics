from django import forms
from django.core.exceptions import ValidationError

from djanalytics import models


class DateRangeReportForm(forms.Form):

    client = forms.ModelChoiceField(
        queryset=models.Client.objects.all(),
        required=False,
    )
    web_property = forms.ModelChoiceField(
        queryset=models.WebProperty.objects.all(),
        required=False,
    )
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    format = forms.ChoiceField(choices=(('html', 'HTML'), ('csv', 'CSV')))

    def clean(self):
        if self.cleaned_data['client'] or self.cleaned_data['web_property']:
            return self.cleaned_data
        raise ValidationError('Select either a client or a web property.')


class DeviceDetailReportForm(DateRangeReportForm):
    device_type = forms.ModelChoiceField(
        queryset=models.DeviceType.objects.all(),
    )
