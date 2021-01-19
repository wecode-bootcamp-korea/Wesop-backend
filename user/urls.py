from django.urls import path
from user.views import UserCheckEmailView, UserSignUpView, UserSignInView

urlpatterns = [
    path('/check', UserCheckEmailView.as_view()),
    path('/signup', UserSignUpView.as_view()),
    path('/signin', UserSignInView.as_view())
]