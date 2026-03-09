from django import forms
from .models import Device, Category

class DeviceSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search devices...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All Categories")
    device_type = forms.ChoiceField(choices=[('', 'All Types')] + Device.DEVICE_TYPES, required=False)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)