from django.contrib.auth.views import LoginView
from django.urls import path, re_path

from .views import LogoutView, RegisterView

app_name = "authorization"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(
            template_name='authorization/login.html',
            redirect_authenticated_user=True,
        ),
        name="login"
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
