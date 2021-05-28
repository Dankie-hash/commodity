from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    path('', include('omega.urls', namespace='omega')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
