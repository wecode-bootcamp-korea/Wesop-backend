from django.urls import path
from .views      import ProductListView, ProductRetrieveView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:id>', ProductRetrieveView.as_view()),
]
