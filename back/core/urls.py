
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

from core import settings
from main.admin import export_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('main.urls')),
    # path('api/v1/students/', include('main.students.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('searchableselect/', include('searchableselect.urls')),
    path('export/', export_admin.urls),
]

schema_view = get_schema_view(
   openapi.Info(
      title="TestSuit API",
      default_version='v1',
      description="TestSuit API documentation",
      terms_of_service="",
      contact=openapi.Contact(email="admin@testsuit.uz"),
      license=openapi.License(name="License"),
   ),
   public=True,
)

urlpatterns += [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)