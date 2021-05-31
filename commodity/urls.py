from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('signup/', views.signup, name='signup'),
    #path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    path('', include('omega.urls', namespace='omega')),
#path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='omega/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetCompleteView.as_view(template_name='omega/password/password_reset_complete.html'),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
