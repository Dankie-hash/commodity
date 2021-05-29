from django.urls import path
from . import views


app_name = 'omega'

urlpatterns = [
            path('', views.index, name='index'),
            path('login/', views.login, name='login'),
            path('logout/', views.logout, name='logout'),
            path('signup/', views.signup, name='signup'),
            path('search/', views.index, name='search'),
            path('node/', views.admin, name='admin'),
            path('categories/', views.CategoryListView.as_view(), name='summary'),
            path('available/', views.AvailableListView.as_view(), name='available'),
            path('category/<int:pk>/', views.unitlist, name='list'),
            path('details/<int:pk>', views.CommodityDetailView.as_view(), name='detail'),
            path('welcome/', views.welcome, name='welcome'),
]