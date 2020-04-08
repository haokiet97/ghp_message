from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include
from accounts import views
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = "ghp-message"
urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('logout', views.user_logout, name='logout'),
    path('messenger/', include('messenger.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
