from django import forms
from .models import Payment


class BuyProductFrom(forms.Form):
    quantity = forms.IntegerField()
    # payment = forms.ModelChoiceField(queryset=Payment.objects.all(), to_field_name='number')
