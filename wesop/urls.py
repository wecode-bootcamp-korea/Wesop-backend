from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('products', include('products.urls'))
]