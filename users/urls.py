from django.urls import path

from users.views import CustomLoginView, CustomLogoutView, IndexView, RegisterView

app_name = "users"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
