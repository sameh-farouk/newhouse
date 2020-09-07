from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, FormView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, SearchableListMixin, SortableListMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PictureInline, ProptyInline, SearchForm
from .models import Listing, Fav, Picture
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ValidationError
# Create your views here.

class Index(ListView):
    model = Listing
    paginate_by = 10

    template_name = 'listings/listings_simple.html'
    def get_queryset(self):
        result = super().get_queryset()
        return result.order_by('-date_created')

    
class ListingDetail(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'
   

class CreateListing(LoginRequiredMixin, CreateWithInlinesView):
    model = Listing
    fields = ['governorate', 'destrict', 'prop_status', 'prop_type', 'price','number_of_bedrooms', 'number_of_baths', 'square_metre', 'contact_details']
    inlines = [PictureInline, ProptyInline]
    template_name = 'listings/new.html'

    def is_valid(self, *args, **kwargs):
        raise ValidationError('yooooo')

    def form_valid(self, form):
        if isinstance(form.instance, Listing):
            form.instance.user = self.request.user
            #if form.instance.pictures.count() < 1:
            #    raise ValidationError('yooooo')

        return super().form_valid(form)


class UpdateListing(LoginRequiredMixin, UpdateWithInlinesView):
    model = Listing
    fields = ['governorate', 'destrict', 'prop_status', 'prop_type', 'price','number_of_bedrooms', 'number_of_baths', 'square_metre', 'contact_details']
    inlines = [PictureInline, ProptyInline]
    template_name = 'listings/new.html'
    def is_valid(self, *args, **kwargs):
        raise ValidationError('yooooo')
    #def get_object(self):
    #    listing= super().get_object()
    #    if listing.user != self.request.user:
    #        raise Http404()
    #    return listing
   
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)





class DeleteListing(LoginRequiredMixin, DeleteView):
    model = Listing
    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        return reverse_lazy('listings:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    



# json api to toggle favorite 
@login_required
def toggleFav(request):
    if request.method == 'POST':
        body=request.body.decode()
        jbody=json.loads(body)    
        list_id = jbody['id']
        
        user = request.user
        if fav:=Fav.objects.filter(user=user, listing_id=list_id).first():
            liked = False
            fav.delete()
            
        else:
            liked = True
            Fav.objects.create(user=user, listing_id=list_id)
        data = {'liked': liked, 'id': list_id}
        return JsonResponse(data, safe=False)


class ListingByStatus(ListView):
    model = Listing
    paginate_by = 10

    template_name = 'listings/listings_simple.html'
    def get_queryset(self):
        status = self.kwargs['status'].upper()
        status_value = Listing.get_value_from_name('Status', status)
        queryset = Listing.objects.filter(prop_status=status_value).all()
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = f"Residential Properties {self.kwargs['status'].replace('_', ' ')}"
        return context

class SearchListings(ListView, FormView):
    form_class = SearchForm
    paginate_by = 10

    template_name = 'listings/listings_advanced.html'
    success_url = reverse_lazy('listings:search_listings')
    #extra_context = {'list_title': 'all results'}
    def get_queryset(self):
        qs = Listing.objects.all()
        return qs
    def form_valid(self, form):
        queryset = Listing.objects.all()
        if prop_status:= self.get_form_kwargs()['data']['prop_status']:
            queryset = queryset.filter(prop_status=prop_status)
        if prop_type:= self.get_form_kwargs()['data']['prop_type']:
            queryset = queryset.filter(prop_type=prop_type)
        if governorate:= self.get_form_kwargs()['data']['governorate']:
            queryset = queryset.filter(governorate=governorate)
        if destrict:= self.get_form_kwargs()['data']['destrict']:
            queryset = queryset.filter(destrict=destrict)
        if number_of_bedrooms:= self.get_form_kwargs()['data']['number_of_bedrooms']:
            queryset = queryset.filter(number_of_bedrooms=number_of_bedrooms)
        if number_of_baths:= self.get_form_kwargs()['data']['number_of_baths']:
            queryset = queryset.filter(number_of_baths=number_of_baths)
        if price:= self.get_form_kwargs()['data']['price']:
            queryset = queryset.filter(price__lte=price)
        if square_metre:= self.get_form_kwargs()['data']['square_metre']:
            queryset = queryset.filter(square_metre__gte=square_metre)
            
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return render(self.request, 'listings/listings_advanced.html', {'object_list': queryset, 'form':self.get_form(), 'list_title': 'Search Results'})

class ListingByUser(ListView):
    model = Listing
    template_name = 'listings/listings_simple.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username=self.kwargs['username'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = f"Listings By {self.kwargs['username']}"
        return context


class UserFavorites(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/listings_simple.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(favorites=user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = "My Favorites"
        return context