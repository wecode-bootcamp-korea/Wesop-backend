from django.urls import path
from .views      import ProductListView, ProductRetrieveView, ProductCreateView, ProductNavView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:id>', ProductRetrieveView.as_view()),
    path('/creation', ProductCreateView.as_view()),
    path('/nav', ProductNavView.as_view()),
]
