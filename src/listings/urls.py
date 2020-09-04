from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import Index, ListingDetail, ListingByStatus, CreateListing, UpdateListing, \
                   Userlistings, DeleteListing, SearchListings, UserFavorites, toggleFav

app_name = 'listings'
urlpatterns = [
path('', Index.as_view(), name='index'),
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>', ListingDetail.as_view(), name='listing_detail'),
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>/edit', UpdateListing.as_view(), name='update_listing'),
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>/delete', DeleteListing.as_view(), name='delete_listing'),
re_path('^(?P<status>for_(sale|rent|timeshare))/$', ListingByStatus.as_view(), name='listing_by_status'),
#path('for_rent/', ListingByStatus.as_view(), name="listing_for_rent"),
#path('for_timeshare/', ListingByStatus.as_view(), name="listing_for_timeshare"),
#path('for_sale/', ListingByStatus.as_view(), name="listing_for_sale"),
path('new/', CreateListing.as_view(), name='new_listing'),
path('users/<str:username>/', Userlistings.as_view(), name='user_listings'),
path('favorites', UserFavorites.as_view(), name='user_favorites'),
path('advanced_search', SearchListings.as_view(), name='search_listings'),
path('api/toggle_fav', toggleFav, name='toggle_fav'),
]