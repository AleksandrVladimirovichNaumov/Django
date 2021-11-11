from django import forms

from products.models import Product
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
