from django import forms
from .models import Car

COLOR_CHOICES = [
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Silver', 'Silver'),
    ('Gray', 'Gray'),
    ('Yellow', 'Yellow'),
]

class CarForm(forms.ModelForm):
    position = forms.IntegerField(label='Position', required=False, min_value=1)
    make = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        fields = ['make', 'color']

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)

        self.fields['color'].widget = forms.Select(choices=COLOR_CHOICES)

        if self.instance and self.instance.pk:
            # Position is set based on the car's position in sorted list
            sorted_cars = list(Car.objects.order_by('key'))
            try:
                position = sorted_cars.index(self.instance) + 1
                self.fields['position'].initial = position
            except ValueError:
                self.fields['position'].initial = None
        else:
            self.fields.pop('position')
