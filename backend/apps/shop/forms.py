from django import forms
from .models import *

class ReviewsForm(forms.ModelForm):

    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(attrs={"class":"form-control"}), empty_label=None
    )

    class Meta:
        model = Reviews
        fields = ('email', 'name', 'text','star')
        widgets = {
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "name": forms.TextInput(attrs={"class":"form-control"}),
            "text": forms.TextInput(attrs={"class":"form-control", "type":"text"}),
        }
