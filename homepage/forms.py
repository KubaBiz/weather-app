from django import forms


class LocationForm(forms.Form):
    latitude = forms.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        widget=forms.NumberInput(attrs={'step': '0.0000001'}),
        min_value=-90, 
        max_value=90,
        error_messages={
            'min_value': 'Latitude must be between -90 and 90 degrees.',
            'max_value': 'Latitude must be between -90 and 90 degrees.'
        }
    )
    longitude = forms.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        widget=forms.NumberInput(attrs={'step': '0.0000001'}),
        min_value=-180, 
        max_value=180,
        error_messages={
            'min_value': 'Longitude must be between -180 and 180 degrees.',
            'max_value': 'Longitude must be between -180 and 180 degrees.'
        }
    )