from os import stat
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # oauth
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('admin/', admin.site.urls),
    path('schema', get_schema_view(
        title="BlogAPI",
        description="API for the BlogAPI",
        version="1.0.0"
    ), name='openapi-schema'),
    
    path('api/', include('blog_api.urls', namespace='blog_api')),

    path('api/user/', include('users.urls', namespace='users')),
    path('docs/', include_docs_urls(title='BlogAPI')),
    path('', include('blog.urls', namespace='blog')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)