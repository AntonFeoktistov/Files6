from django.urls import path

from files.views import HomeView

app_name = "files"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
