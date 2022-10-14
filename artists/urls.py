from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    #path('', index, name='home'),
    #path('', cache_page(60)(ArtistsHome.as_view()), name='home'), #Здесь подключено кэширование главной страницы в течение 60 с
    path('', ArtistsHome.as_view(), name='home'),
    path('about/', about, name = 'about'),
    #path('addpage/', addpage, name='addpage'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    # path('contact/', contact, name='contact'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    #path('login/', login, name = 'login'),
    path('login/', LoginUser.as_view(), name = 'login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name = 'register'),
    #path('cats/<slug:cat_slug>/', categories, name='cats'),
    path('cats/<slug:cat_slug>/', ArtistsCategory.as_view(), name='cats'),
    #path('post/<slug:post_slug>/', show_post, name='post')
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post')
]
