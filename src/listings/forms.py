from extra_views import InlineFormSetFactory
from .models import Picture, Propty, Listing, Destrict, Governorate
from django import forms

class PictureInline(InlineFormSetFactory):
    model = Picture
    fields = '__all__'
    factory_kwargs={'can_delete': True}

class ProptyInline(InlineFormSetFactory):
    model = Propty
    fields = '__all__'
    factory_kwargs={'can_delete': False}    


class SearchForm(forms.ModelForm):
    destrict = forms.ModelChoiceField(label="destirct", queryset=Destrict.objects.all(), empty_label="All")
    governorate = forms.ModelChoiceField(label="governorate", queryset=Governorate.objects.all(), empty_label="All")
    prop_status = forms.ChoiceField(label="status", choices=[('', 'All')]  + Listing.Status.choices)
    prop_type = forms.ChoiceField(label="type", choices=[('', 'All')]  + Listing.Type.choices)

    class Meta:
        model = Listing
        fields = ['prop_type', 'prop_status' ,'governorate', 'destrict', 'number_of_bedrooms', 'number_of_baths', 'square_metre', 'price']
        labels = {
        "price": "Price [at most..]",
        "square_metre":"area [at least..]",
        "prop_type": "property type",
        "prop_status": "property status"
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.required = False