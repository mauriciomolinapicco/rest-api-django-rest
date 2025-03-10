from django.urls import path
from . import views

product_mixin_view = views.ProductMixinView.as_view()

urlpatterns = [
    path('<int:pk>/', product_mixin_view, name='product-detail'),
    path('<int:pk>/update/', product_mixin_view),
    path('<int:pk>/delete/', product_mixin_view),
    path('', views.ProductListCreateAPIView.as_view(), name='product-list')
]