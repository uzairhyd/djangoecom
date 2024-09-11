
from django.urls import path
  
from .views import (
    ProductListView, 
    #ProductDetailView,
    ProductDetailSlugView,
    #ProductFeaturedListView,
    #ProductFeaturedDetailView
    )

urlpatterns = [
    path('', ProductListView.as_view()),
    #path('featured/', ProductFeaturedListView.as_view()),
    #path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    #path('products/<int:pk>/', ProductDetailView.as_view()),
    path('<slug:slug>/', ProductDetailSlugView.as_view()),
]
