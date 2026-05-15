from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('account/', include('allauth.urls')),
    path('about/<int:pk>/', about, name='about'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),
    path('category/<slug:slug>/', category, name='category'),
    path('technology/', technology, name='technology'),
    path('fashion/', fashion, name='fashion'),
    path('foods/', foods, name='foods'),
    path('gaming/', gaming, name='gaming'),
    path('sports/', sports, name='sports'),
    path('politics/', politics, name='politics'),
    path('search/', search, name='search'),
    path('category_view/', category_view, name='category_view'),
]