from django.urls import path
from . import views

urlpatterns = [
    path("products/",views.ProductView.as_view()),
    path("products/model",views.ProductView.as_view()),
    
]