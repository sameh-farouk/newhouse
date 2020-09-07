from django.urls import path, include, re_path
from django.views.generic import TemplateView
from .views import Index, ListingDetail, ListingByStatus, CreateListing, UpdateListing, \
                   ListingByUser, DeleteListing, SearchListings, UserFavorites, toggleFav

app_name = 'listings'
urlpatterns = [
path('', Index.as_view(), name='index'),
# create listing
path('new/', CreateListing.as_view(), name='new_listing'),
# read listing detalis
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>', ListingDetail.as_view(), name='listing_detail'),
# update listing
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>/edit', UpdateListing.as_view(), name='update_listing'),
# delete listing
path('<str:status>/<str:governorate>/<str:destrict>/<str:type>,<int:pk>/delete', DeleteListing.as_view(), name='delete_listing'),
# filter listings by property status
# for_rent/
# for_timeshare/
# for_sale/
re_path('^(?P<status>for_(sale|rent|timeshare))/$', ListingByStatus.as_view(), name='listing_by_status'),
# show user own listings
path('users/<str:username>/', ListingByUser.as_view(), name='user_listings'),
# show user favourite listings
path('favorites', UserFavorites.as_view(), name='user_favorites'),
# show and do advanced filters or serach
path('advanced_search', SearchListings.as_view(), name='search_listings'),
# api json end point to update user favourite status for listings
path('api/toggle_fav', toggleFav, name='toggle_fav'),
]