# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('api/templates/', include('templates_app.urls')),
#     path('api/leads/', include('leads_app.urls')),
#     path('api/email/', include('emails_app.urls')),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('test/', views.sample_view, name='email-home'),
    path('admin/', admin.site.urls),
    path('templates/', include('templates_app.urls')),  # <-- this line is key
     path('sendEmail/', include('emails_app.urls')),
     path('api/', include('leads_app.urls')),

]
