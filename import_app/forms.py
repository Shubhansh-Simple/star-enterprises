# import_app/forms.py

# django
from django import forms

# local
from .models import Imports


class ImportCreateForm(forms.ModelForm):
    '''Form for adding stock in current stock'''

    class Meta:
        model  = Imports
        fields = ['items','import_quantity'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update first item label in SELECT widget
        self.fields['items'].empty_label = 'Choose Your Item'


class ImportUpdateForm(forms.ModelForm):
    '''Form for updating imported stock'''

    class Meta:
        model  = Imports
        fields = ['items','import_quantity'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Items selection cannot be changed ( Update View )
        self.fields['items'].required                 = False
        self.fields['items'].widget.attrs['disabled'] = True
