"""
URL configuration for SWAN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_not_required
from django.urls import path, include, re_path
from django.views.static import serve

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

from swan import settings

admin.site.site_header = 'SWAN Admin'
admin.site.site_title = 'SWAN Admin Portal'
admin.site.index_title = 'Welcome to SWAN'

@login_not_required
def free_serve(request, path, **kwargs):
    return serve(request, path, **kwargs)

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    path('v1/', include('app.urls')),

    path('', free_serve, {'path': 'index.html', 'document_root': settings.STATIC_ROOT}),
    path('favicon.ico', free_serve, {'path': 'favicon.ico', 'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
    ]

# TODO should be done by nginx
if not settings.DEBUG:
    urlpatterns += [re_path('static/(?P<path>.*)', free_serve, {'document_root': settings.STATIC_ROOT})]

urlpatterns += [re_path('assets/(?P<path>.*)', free_serve, {'document_root': settings.STATIC_ROOT / "assets"})]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
