from django.urls import path
from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:id>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
] 