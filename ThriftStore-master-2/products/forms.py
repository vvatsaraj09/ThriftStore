from django import forms
from .models import Product

class CreateProductForm(forms.ModelForm):
    seller = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date = forms.DateField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    lattitude = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.DecimalField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Product
        fields = '__all__'

