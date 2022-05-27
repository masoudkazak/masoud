from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_swagger_view(title='Pastebin API')

schema_view2 = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('cv-masoud-admin/', admin.site.urls),
    path('', include('item.urls')),
    path('api/', include('api.urls')),
    path('', include('account.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', schema_view),
    path('redoc/', schema_view2.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
