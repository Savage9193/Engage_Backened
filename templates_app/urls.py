from django.urls import path
from .views import TemplateListCreateView, TemplateDeleteView

urlpatterns = [
     path('', TemplateListCreateView.as_view(), name='list-create-template'),  
    path('template/', TemplateListCreateView.as_view(), name='list-create-template'),
    path('<str:template_id>/delete/', TemplateDeleteView.as_view(), name='delete-template'),
]
