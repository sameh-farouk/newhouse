from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView 
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.forms.models import BaseInlineFormSet
from .forms import ProfileInline
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

# Create your views here.

class ProfileView(DetailView):
    template_name="accounts/profile.html"
    model = get_user_model()
    def get_object(self, queryset=None):
        return self.request.user
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['has_verified_email'] = self.request.user.profile.account_verified()
        return context


class ProfileEdit(UpdateWithInlinesView):
    model = get_user_model()
    inlines = [ProfileInline]
    fields = ['first_name', 'last_name']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    def get_object(self, queryset=None):
        return self.request.user
    



