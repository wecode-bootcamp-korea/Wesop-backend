from django.urls import path
from .views      import ProductView, ProductCategoryView, ProductsView

urlpatterns = [
    path('', ProductsView.as_view()),
    path('/<int:id>', ProductView.as_view()),
    path('/category', ProductCategoryView.as_view()),
]