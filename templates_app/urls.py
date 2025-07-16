from django.urls import path
from .views import TemplateListCreateView, TemplateDeleteView, TemplateEditView

urlpatterns = [
    path('', TemplateListCreateView.as_view(), name='list-create-template'),  
    path('template/', TemplateListCreateView.as_view(), name='list-create-template'),
    path('<str:template_id>/delete/', TemplateDeleteView.as_view(), name='delete-template'),
    path('<str:template_id>/edit/', TemplateEditView.as_view(), name='edit-template'),
]
