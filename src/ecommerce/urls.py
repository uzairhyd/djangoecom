"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
  
# from products.views import (
#     ProductListView, 
#     ProductDetailView,
#     ProductDetailSlugView,
#     ProductFeaturedListView,
#     ProductFeaturedDetailView
#     )

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
    path('',home_page),
    path('about/',about_page),
    path('contact/',contact_page),
    path('login/', login_page),
    path('register/', register_page),
    path('products/', include('products.urls')),
    # path('products/', ProductListView.as_view()),
    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    # #path('products/<int:pk>/', ProductDetailView.as_view()),
    # path('products/<slug:slug>/', ProductDetailSlugView.as_view()),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)