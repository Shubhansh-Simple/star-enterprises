# items/forms.py

# django
from django import forms

# local
from .models import Items


class ItemForm(forms.ModelForm):
    '''Form for CRUD operations of items model'''

    class Meta:
        model  = Items
        fields = ['name','price','is_active']

    def clean_name(self):
        '''Item name should be title case'''

        name_input = self.cleaned_data.get('name')

        # If name DoesNotExist
        if not name_input:
            raise forms.ValidationError('Item\'s name is required')

        # Title case
        name_input = name_input.title()

        return name_input

