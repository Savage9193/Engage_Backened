from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
import pandas as pd
import io
from django.db import transaction

# Create your models here.

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-id')  # Order by newest first
    serializer_class = CustomerSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        # Get query parameters
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)
        
        # Validate page_size
        try:
            page_size = int(page_size)
            if page_size < 1 or page_size > 100:
                page_size = 10
        except ValueError:
            page_size = 10
        
        # Get queryset
        queryset = self.get_queryset()
        
        # Apply pagination
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page)
        except:
            page_obj = paginator.page(1)
        
        # Serialize data
        serializer = self.get_serializer(page_obj.object_list, many=True)
        
        return Response({
            'message': 'Customers fetched successfully',
            'data': serializer.data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_records': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            }
        }, status=status.HTTP_200_OK)

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
        filters = request.data.get('filters', {})
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 10)
        
        # Validate page_size
        try:
            page_size = int(page_size)
            if page_size < 1 or page_size > 100:
                page_size = 10
        except ValueError:
            page_size = 10
        
        # Apply filters
        queryset = Customer.objects.all().order_by('-id')
        
        if filters:
            # Handle special cases for filtering
            filter_kwargs = {}
            for key, value in filters.items():
                if value:  # Only apply non-empty filters
                    if key in ['year', 'final_date', 'annual_income', 'loan_amount']:
                        # Integer fields
                        try:
                            filter_kwargs[key] = int(value)
                        except (ValueError, TypeError):
                            continue
                    elif key in ['employment_length', 'interest_rate', 'debt_to_income_ratio', 'total_payment', 'total_principle_to_recover', 'total_recoveries', 'installment']:
                        # Float fields
                        try:
                            filter_kwargs[key] = float(value)
                        except (ValueError, TypeError):
                            continue
                    else:
                        # String fields - use icontains for partial matching
                        filter_kwargs[f'{key}__icontains'] = value
            
            queryset = queryset.filter(**filter_kwargs)
        
        # Apply pagination
        paginator = Paginator(queryset, page_size)
        
        try:
            page_obj = paginator.page(page)
        except:
            page_obj = paginator.page(1)
        
        # Serialize data
        serializer = CustomerSerializer(page_obj.object_list, many=True)
        
        return Response({
            'message': 'Filtered customers fetched successfully',
            'data': serializer.data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'total_records': paginator.count,
                'page_size': page_size,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            }
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
            
            # Determine the appropriate message based on results
            if created_count == 0 and error_count > 0:
                if all('already exists' in error for error in errors):
                    message = f'All {error_count} customers already exist in the system. No new customers were added.'
                else:
                    message = f'No new customers were created. {error_count} errors encountered.'
            elif created_count > 0 and error_count > 0:
                # Check how many errors are duplicates
                duplicate_errors = [error for error in errors if 'already exists' in error]
                duplicate_count = len(duplicate_errors)
                other_errors_count = error_count - duplicate_count
                
                if duplicate_count > 0 and other_errors_count == 0:
                    # All errors are duplicates
                    message = f'Successfully added {created_count} new customer(s). {duplicate_count} customer(s) were skipped as they already exist.'
                elif duplicate_count > 0 and other_errors_count > 0:
                    # Mixed errors - some duplicates, some other issues
                    message = f'Successfully added {created_count} new customer(s). {duplicate_count} customer(s) were skipped as duplicates, {other_errors_count} entries had other issues.'
                else:
                    # No duplicates, only other errors
                    message = f'Successfully added {created_count} new customer(s). {error_count} entries had issues.'
            elif created_count > 0 and error_count == 0:
                message = f'Successfully imported {created_count} customer(s) from Excel file.'
            else:
                message = 'Excel file processed but no customers were created.'
            
            return Response({
                'message': message,
                'created_count': created_count,
                'error_count': error_count,
                'errors': errors[:10] if errors else []  # Limit error messages
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Unexpected error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
