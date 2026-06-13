from django.urls import path

from files.views import FolderCreateView, HomeView

app_name = "files"

urlpatterns = [
    path(
        "<path:current_path>/create-folder",
        FolderCreateView.as_view(),
        name="create_folder",
    ),
    path("<path:current_path>", HomeView.as_view(), name="home"),
]
