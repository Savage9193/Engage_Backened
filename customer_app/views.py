from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.views import APIView

# Create your views here.

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Customer created successfully',
            'data': response.data
        }, status=status.HTTP_201_CREATED)

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message': 'Customer updated successfully',
            'data': response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'Customer deleted successfully'
        }, status=status.HTTP_200_OK)

class CustomerFilterView(APIView):
    def post(self, request, *args, **kwargs):
        filters = request.data
        queryset = Customer.objects.filter(**filters)
        serializer = CustomerSerializer(queryset, many=True)
        return Response({
            'message': 'Filtered customers fetched successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
