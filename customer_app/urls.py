from django.urls import path
from .views import CustomerListCreateView, CustomerRetrieveUpdateDestroyView, CustomerFilterView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:id>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),
    path('customers/filter/', CustomerFilterView.as_view(), name='customer-filter'),
] 