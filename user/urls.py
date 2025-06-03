from django.urls import path
from .views import RegisterView, RetrieveUserView,LoginView, LogoutView, UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('retrieve', RetrieveUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('update-profile/', UserUpdateView.as_view()),
]
