# from django.urls import path
# from . import views
# from django.contrib import admin
# from django.urls import path, include



# urlpatterns = [
#     path('test/', views.sample_view, name='email-home'),
#     path('admin/', admin.site.urls),
#     path('templates/', include('templates_app.urls')),  # <-- this line is key
#      path('sendEmail/', include('emails_app.urls')),
#      path('api/', include('leads_app.urls')),

# ]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('test/', views.sample_view, name='email-home'),
    path('admin/', admin.site.urls),
    path('templates/', include('templates_app.urls')),
    path('sendEmail/', include('emails_app.urls')),
    path('api/', include('leads_app.urls')),
    path('api/', include('customer_app.urls')),
    path('templates_app/', include('templates_app.urls')),
]

# ✅ Serve media files during development

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
