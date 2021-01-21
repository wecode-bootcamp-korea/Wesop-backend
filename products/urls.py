from django.urls import path
from products.views import ProductListView, ProductView

urlpatterns = [
    path('/product', ProductListView.as_view()),
    path('/product/<int:product_id>', ProductView.as_view())
]

