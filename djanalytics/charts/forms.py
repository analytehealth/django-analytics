from django import forms

from djanalytics import models


class ClientModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.name


class DateRangeForm(forms.Form):

    client = ClientModelChoiceField(
        queryset=models.Client.objects.all(),
        empty_label=None,
        to_field_name='uuid',
    )
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


class PageViewChartForm(DateRangeForm):
    start_page = forms.CharField(required=False)
