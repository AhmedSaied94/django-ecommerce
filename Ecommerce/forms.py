from random import choices
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

payment_methods = (
    ('C', 'cash'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Address'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'City'}))
    country = CountryField(blank_label='Select Country').formfield(widget=forms.Select(attrs={'class':'form-control'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Zip Code'}))
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Telephone'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'input', 'placeholder':'Order notes'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=payment_methods)
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id':'save_info'}))
    accept_terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id':'terms'}))


