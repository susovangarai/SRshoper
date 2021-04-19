from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    choices = forms.ChoiceField()

    class Meta:
        model = Category
        fields = ('name',)


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'
