from drf_yasg import openapi
from django.conf import settings
from django.contrib  import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.conf.urls.static  import static
from rest_framework.routers import DefaultRouter

from library.views import *

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Library-API",
        default_version='v1',
        description="API for Library",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# ViewSets
router = DefaultRouter()
router.register('comments', CommentViewSet)
router.register('books', BookViewSet)
router.register('ratings', RatingViewSet)
router.register('orders', OrderViewSet)

# Routes
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('library/', include(router.urls)),
    path('account/', include('account.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# sudo systemctl restart nginx
# sudo systemctl restart gunicorn
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn

# celery -A main beat
# celery -A main worker -l INFO --pool=solo
