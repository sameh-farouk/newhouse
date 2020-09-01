from django.urls import path, include
from django.views.generic import TemplateView
from .views import ProfileView, ProfileEdit
app_name = 'accounts'

urlpatterns = [
path("", TemplateView.as_view(template_name="accounts/index.html"), name="index"),
path("profile/", ProfileView.as_view(), name="profile"),
path("profile/edit/", ProfileEdit.as_view(), name="profile_edit"),
]

