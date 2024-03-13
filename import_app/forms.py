# import_app/forms.py

# django
from django import forms

# local
from .models import Imports


class ImportCreateForm(forms.ModelForm):
    '''Form for importing items'''

    class Meta:
        model  = Imports
        fields = ['items','import_quantity'] 


class ImportUpdateForm(forms.ModelForm):
    '''Form for importing items'''

    class Meta:
        model  = Imports
        fields = ['items','import_quantity'] 
