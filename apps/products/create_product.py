from django import forms
from .models import Category


class CreateProductForm(forms.Form):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='name')
    price = forms.FloatField()
    discount = forms.IntegerField(initial=0)
