from django.http import JsonResponse

def sample_view(request):
    return JsonResponse({"message": "Hello from engage_backend!"})
