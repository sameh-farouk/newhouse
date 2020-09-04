from extra_views import InlineFormSetFactory
from .models import Picture, Propty, Listing
from django.forms import ModelForm

class PictureInline(InlineFormSetFactory):
    model = Picture
    fields = '__all__'
    factory_kwargs={'can_delete': True}

class ProptyInline(InlineFormSetFactory):
    model = Propty
    fields = '__all__'
    factory_kwargs={'can_delete': False}    


class SearchForm(ModelForm):

    class Meta:
        model = Listing
        fields = ['prop_type', 'prop_status' ,'governorate', 'destrict', 'number_of_bedrooms', 'number_of_baths']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (field_name, field) in self.fields.items():
            field.required = False