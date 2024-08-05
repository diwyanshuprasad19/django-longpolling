from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Import your views
from example import views

urlpatterns = [
    path('', views.test, name='home'),
    path('trigger/', views.trigger, name='trigger'),
    path('poll/', views.poll, name='poll'),

    # Uncomment the following lines to enable the admin:
    # path('admin/', admin.site.urls),
]

# Serve static files in development (not for production use)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
