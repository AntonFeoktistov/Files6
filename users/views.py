from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views import View

from users.forms import SignUpForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("files:home")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    next_page = "files:home"


class CustomLogoutView(LogoutView):
    next_page = "files:home"


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("files:home")
        return redirect("users:login")
