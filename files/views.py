from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class HomeView(LoginRequiredMixin, View):
    template_name = "files/home.html"
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request):
        return render(
            request,
            self.template_name,
        )
