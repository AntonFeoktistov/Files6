from dataclasses import dataclass

from django.urls import reverse


@dataclass(frozen=True, slots=True)
class Urls:
    home_url: str
    login_url: str
    logout_url: str
    register_url: str

    @property
    def referer(self) -> str:
        return self.home_url


urls = Urls(
    home_url=reverse("files:home"),
    login_url=reverse("users:login"),
    logout_url=reverse("users:logout"),
    register_url=reverse("users:register"),
)
