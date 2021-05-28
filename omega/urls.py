from django.urls import path
from . import views


app_name = 'omega'

urlpatterns = [
            path('', views.index, name='index'),
            path('login/', views.login, name='login'),
            path('signup/', views.signup, name='signup'),
            path('search/', views.index, name='search'),
path('node/', views.admin, name='admin'),
            path('categories/', views.summary, name='summary'),
            path('available/', views.available, name='available'),
            path('categ/', views.list, name='list'),
path('categ2/', views.list2, name='list2'),
path('categ3/', views.list3, name='list3'),
path('categ4/', views.list4, name='list4'),

            path('detail/', views.detail, name='detail'),
]