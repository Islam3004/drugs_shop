from django import forms
from .models import *
import django_filters

class ReviewsForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(attrs={"class":"form-control"}), empty_label=None
    )
    class Meta:
        model = Reviews
        fields = ('text','star')
        widgets = {
            "text": forms.TextInput(attrs={"class":"form-control", "type":"text"}),
        }


#
# class ProductFilter(django_filters.FilterSet):
#     price = django_filters.NumberFilter()
#     price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
#     price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
#
#     class Meta:
#         model = Products