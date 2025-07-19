from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
import io
from django.db import transaction

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

class CustomerExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        try:
            if 'file' not in request.FILES:
                return Response({
                    'error': 'No file uploaded'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            excel_file = request.FILES['file']
            
            # Check file extension
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return Response({
                    'error': 'Please upload a valid Excel file (.xlsx or .xls)'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Read Excel file
            try:
                df = pd.read_excel(excel_file)
            except Exception as e:
                return Response({
                    'error': f'Error reading Excel file: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate required columns
            required_columns = [
                'year', 'issue_date', 'final_date', 'employment_length', 
                'home_ownership', 'income_category', 'annual_income', 
                'loan_amount', 'term', 'application_type', 'purpose', 
                'interest_payments', 'loan_condition', 'interest_rate', 
                'grade', 'debt_to_income_ratio', 'total_payment', 
                'total_principle_to_recover', 'total_recoveries', 
                'installment', 'region', 'Email', 'name'
            ]
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return Response({
                    'error': f'Missing required columns: {", ".join(missing_columns)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Process data and create customers
            created_count = 0
            error_count = 0
            errors = []
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Convert NaN to None for optional fields
                        customer_data = {}
                        for col in required_columns:
                            value = row[col]
                            if pd.isna(value):
                                if col in ['year', 'final_date', 'annual_income', 'loan_amount']:
                                    value = 0
                                elif col in ['employment_length', 'interest_rate', 'debt_to_income_ratio', 'total_payment', 'total_principle_to_recover', 'total_recoveries', 'installment']:
                                    value = 0.0
                                else:
                                    value = ''
                            customer_data[col] = value
                        
                        # Check if customer with this email already exists
                        if Customer.objects.filter(Email=customer_data['Email']).exists():
                            error_count += 1
                            errors.append(f"Row {index + 1}: Customer with email {customer_data['Email']} already exists")
                            continue
                        
                        # Create customer
                        customer = Customer.objects.create(**customer_data)
                        created_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        errors.append(f"Row {index + 1}: {str(e)}")
                        continue
            
            return Response({
                'message': 'Excel file processed successfully',
                'created_count': created_count,
                'error_count': error_count,
                'errors': errors[:10] if errors else []  # Limit error messages
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Unexpected error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
