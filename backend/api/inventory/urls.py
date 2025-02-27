from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

urlpatterns = [
    path("products/",views.ProductView.as_view()),
    path("products/<int:id>/",views.ProductView.as_view()),
    path("purchase/",views.PurchaseView.as_view()),
    path("sales/",views.SalesView.as_view()),
    path("products/model",views.ProductModelViewSet.as_view({'get': 'list','post': 'create'})),
    path("productrs/model/",views.ProductModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('inventories/<int:id>/',views.InventoryView.as_view()),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('login/', views.LoginView.as_view()),
    path('retry/', views.RetryView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('sync/',views.SalesSyncViews.as_view()),
    path('async/',views.SalesAsyncViews.as_view()),
    path('summary/',views.SalesList.as_view()),
]
