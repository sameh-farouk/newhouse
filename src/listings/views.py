from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, FormView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, SearchableListMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PictureInline, ProptyInline, SearchForm
from .models import Listing, Fav
from django.http import Http404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import json

# Create your views here.

class Index(SearchableListMixin, ListView):
    model = Listing
    template_name = 'listings/index.html'
    search_fields = ['destrict__name', 'governorate__name','propty__address']
    def get_queryset(self):
        result = super().get_queryset()
        return result.order_by('-date_created')[:10]

    
class ListingDetail(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'


class ListingByStatus(ListView):
    model = Listing
    template_name = 'listings/listings.html'
    def get_queryset(self):
        status = self.kwargs['status'].upper()
        status_value = Listing.get_value_from_name('Status', status)
        queryset = Listing.objects.filter(prop_status=status_value).all()
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = f"Browse residential Properties {self.kwargs['status'].replace('_', ' ')}"
        return context
    


class CreateListing(LoginRequiredMixin, CreateWithInlinesView):
    model = Listing
    fields = ['governorate', 'destrict', 'prop_status', 'prop_type', 'price','number_of_bedrooms', 'number_of_baths', 'square_metre']
    inlines = [PictureInline, ProptyInline]
    template_name = 'listings/new.html'
    def form_valid(self, form):
        if isinstance(form.instance, Listing):
            form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateListing(LoginRequiredMixin, UpdateWithInlinesView):
    model = Listing
    fields = ['governorate', 'destrict', 'prop_status', 'prop_type', 'price','number_of_bedrooms', 'number_of_baths', 'square_metre']
    inlines = [PictureInline, ProptyInline]
    template_name = 'listings/new.html'
    
    #def get_object(self):
    #    listing= super().get_object()
    #    if listing.user != self.request.user:
    #        raise Http404()
    #    return listing
   
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class Userlistings(ListView):
    model = Listing
    template_name = 'listings/listings.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username=self.kwargs['username'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = f"Browse residential Properties By {self.kwargs['username']}"
        return context


class DeleteListing(LoginRequiredMixin, DeleteView):
    model = Listing
    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        return reverse_lazy('listings:index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    

class UserFavorites(ListView):
    model = Listing
    template_name = 'listings/listings.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(favorites=user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_title"] = "My Favorites"
        return context

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




class SearchListings(ListView, FormView):
    form_class = SearchForm
    template_name = 'listings/search_form.html'
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

        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return render(self.request, 'listings/search_form.html', {'object_list': queryset, 'form':self.get_form(), 'list_title': 'Search Results'})