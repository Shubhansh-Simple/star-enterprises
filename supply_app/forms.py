# supply_app/forms.py

# django
from django import forms

# local
from .models import Supplys


class SupplyCreateForm(forms.ModelForm):
    '''Form for supplying stock from current stock'''

    class Meta:
        model  = Supplys
        fields = ['items','quantity'] 
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update first item label in SELECT widget
        self.fields['items'].empty_label = 'Choose Your Item'


class SupplyUpdateForm(forms.ModelForm):
    '''Form for updating supplied stock'''

    class Meta:
        model  = Supplys
        fields = ['items','quantity'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Items selection cannot be changed ( Update View )
        self.fields['items'].required                 = False
        self.fields['items'].widget.attrs['disabled'] = True