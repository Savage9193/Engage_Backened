# Excel Upload Feature for Customer Data

## Overview
This feature allows you to upload Excel files (.xlsx or .xls) containing customer data to bulk import customers into the system.

## API Endpoint
- **URL**: `/api/customers/upload-excel/`
- **Method**: POST
- **Content-Type**: multipart/form-data

## Required Excel Columns
Your Excel file must contain the following columns (case-sensitive):

1. `year` - Integer
2. `issue_date` - String
3. `final_date` - Integer
4. `employment_length` - Float
5. `home_ownership` - String
6. `income_category` - String
7. `annual_income` - Integer
8. `loan_amount` - Integer
9. `term` - String
10. `application_type` - String
11. `purpose` - String
12. `interest_payments` - String
13. `loan_condition` - String
14. `interest_rate` - Float
15. `grade` - String
16. `debt_to_income_ratio` - Float
17. `total_payment` - Float
18. `total_principle_to_recover` - Float
19. `total_recoveries` - Float
20. `installment` - Float
21. `region` - String
22. `Email` - String (must be unique)
23. `name` - String

## Usage Examples

### Using cURL
```bash
curl -X POST \
  http://localhost:8000/api/customers/upload-excel/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/customers.xlsx'
```

### Using Python requests
```python
import requests

url = 'http://localhost:8000/api/customers/upload-excel/'
files = {'file': open('customers.xlsx', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

### Using JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/customers/upload-excel/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Response Format

### Success Response
```json
{
    "message": "Excel file processed successfully",
    "created_count": 150,
    "error_count": 2,
    "errors": [
        "Row 45: Customer with email john@example.com already exists",
        "Row 67: Invalid data format"
    ]
}
```

### Error Response
```json
{
    "error": "Missing required columns: Email, name"
}
```

## Validation Rules

1. **File Format**: Only .xlsx and .xls files are accepted
2. **Required Columns**: All 23 columns must be present
3. **Email Uniqueness**: Each email must be unique in the system
4. **Data Types**: 
   - Integer fields: `year`, `final_date`, `annual_income`, `loan_amount`
   - Float fields: `employment_length`, `interest_rate`, `debt_to_income_ratio`, `total_payment`, `total_principle_to_recover`, `total_recoveries`, `installment`
   - String fields: All other fields

## Error Handling

- **Missing File**: Returns 400 error if no file is uploaded
- **Invalid Format**: Returns 400 error for non-Excel files
- **Missing Columns**: Returns 400 error with list of missing columns
- **Duplicate Emails**: Skips rows with duplicate emails and reports them
- **Invalid Data**: Skips rows with invalid data and reports errors
- **Database Errors**: Uses transaction rollback to prevent partial imports

## Notes

- The system processes the Excel file row by row
- If a row has an error, it's skipped but other rows continue processing
- Empty cells are handled automatically (integers become 0, floats become 0.0, strings become empty)
- The response includes a count of successfully created customers and any errors encountered
- Only the first 10 errors are returned in the response to prevent overwhelming responses 