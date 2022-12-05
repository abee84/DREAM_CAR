from django import forms
from django import forms
from cars.models import Car

class AddCarForm(forms.ModelForm):
    class Meta:
        model= Car
        fields=['car_title','state','city','color','model','year','condition','price', 'description', 'car_photo', 'features', 'body_style', 
        'engine', 'transmission', 'interiors', 'kilometers_driven', 'doors', 'no_passengers', 'vin_no', 'mileage', 'fuel_type', 'no_owners', 'is_featured', 'created_date']


class UpdateCarForm(forms.ModelForm):
        class Meta:
                model= Car
                fields=['car_title','state','city','color','model','year','condition','price', 'description', 'car_photo', 'features', 'body_style',
                'engine', 'transmission', 'interiors', 'kilometers_driven', 'doors', 'no_passengers', 'vin_no', 'mileage', 'fuel_type', 'no_owners', 'is_featured', 'created_date']

       