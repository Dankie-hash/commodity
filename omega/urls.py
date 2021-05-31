from django.urls import path
from . import views


app_name = 'omega'

urlpatterns = [
            path('', views.index, name='index'),
            path('login/', views.login, name='login'),
            path('logout/', views.logout, name='logout'),
            path('signup/', views.signup, name='signup'),
            path('search/', views.search, name='search'),
            path('profile/', views.profile, name='profile'),
            path('profile/update/', views.update, name='uprofile'),
            path('categories/', views.CategoryListView.as_view(), name='summary'),
            path('available/', views.AvailableListView.as_view(), name='available'),
            path('category/<int:pk>/', views.unitlist, name='list'),
            path('details/<int:pk>', views.CommodityDetailView.as_view(), name='detail'),
            path('contact/', views.contact, name='contact'),
            path("password_reset", views.password_reset_request, name="password_reset"),
]