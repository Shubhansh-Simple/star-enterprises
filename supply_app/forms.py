# supply_app/forms.py

# django
from django import forms

# local
from .models      import Supplys
from items.models import Items


class SupplyCreateForm(forms.ModelForm):
    '''Form for supplying stock from current stock'''

    class Meta:
        model  = Supplys
        fields = ['items', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update first item label in SELECT widget
        self.fields['items'].empty_label = 'Choose Your Item To Supply'

        # Only those whose quantity > 0
        self.fields['items'].queryset    = Items.objects.filter(quantity__gt=0)


    def clean_quantity(self):
        '''Quantity should be greater than 0 and less than equal to current stock quantity'''

        print("CLEANED DATA - ",self.cleaned_data)

        quantity_input = self.cleaned_data.get('quantity')

        # Quantity should be positive number
        if quantity_input < 1:
            raise forms.ValidationError('Quantity must be a positive number')

        item_input = self.cleaned_data.get('items')

        # Items does not exist in our model
        if not item_input:
            raise forms.ValidationError(f'Enter a valid available choice')

        # Supplied quantity should be lesser than equal to current quantity
        if quantity_input > item_input.quantity:
            raise forms.ValidationError(f'We have only {item_input.quantity} box left')

        return quantity_input


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


    def clean_quantity(self):
        '''Quantity should be greater than 0 and less than equal to current stock quantity'''

        print("CLEANED DATA - ",self.cleaned_data)

        quantity_input = self.cleaned_data.get('quantity')

        # Quantity should be positive number
        if quantity_input < 1:
            raise forms.ValidationError('Quantity must be a positive value')

        '''
        item_input = self.cleaned_data.get('items')

        # Items does not exist in our model
        if not item_input:
            raise forms.ValidationError(f'Enter a valid available choice')

        # Supplied quantity should be lesser than equal to current quantity
        if quantity_input > item_input.quantity:
            raise forms.ValidationError(f'We have only {item_input.quantity} box left')
        '''

        return quantity_input


