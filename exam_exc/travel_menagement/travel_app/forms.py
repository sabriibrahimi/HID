from django import forms

from .models import Trip

class AddForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model=Trip
        exclude = ['guide', ]