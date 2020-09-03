from django import forms

from products.models import Product, ProductRating


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']


class RawProductForm(forms.Form):
    name = forms.CharField()
    price = forms.IntegerField(initial=10)
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Something..."}))


class RateForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ['rate', ]
