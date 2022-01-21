from django.urls import path
from .views import *

app_name = 'item'


urlpatterns = [
    path('', ItemListView.as_view(), name='list'),
    path('item/create/', ItemCreateView.as_view(), name='create'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='delete'),
    path('item/order/<int:pk>/', OrderItemView.as_view(), name="orderitem"),
    path("item/basket/<int:pk>/", BasketView.as_view(), name="basket"),
    path("address/", AddressView.as_view(), name="address"),
    path("address/<int:pk>/", AddressUpdateView.as_view(), name="addressupdate"),
]
