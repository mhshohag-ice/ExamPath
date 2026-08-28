from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.admin_views import admin_dashboard

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('exams/', include('exams.urls')),
    path('questions/', include('questions.urls')),
    path('quiz/', include('quiz.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('bookmarks/', include('bookmarks.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('gamification.urls')),
    path('imports/', include('imports_app.urls')),
]

handler404 = 'core.views.handler404'
handler403 = 'core.views.handler403'
handler500 = 'core.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
