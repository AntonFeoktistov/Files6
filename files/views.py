from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from files.forms import FileUploadForm
from files.models import File


class HomeView(LoginRequiredMixin, View):
    template_name = "files/home.html"
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request):
        user_files = File.objects.filter(user=request.user).order_by("-created_at")

        form = FileUploadForm()

        context = {"form": form, "files": user_files}
        return render(request, self.template_name, context)

    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.save()
            messages.success(request, "Файл успешно загружен и сохранён!")
            return redirect("files:home")
        else:
            user_files = File.objects.filter(user=request.user).order_by("-created_at")

            context = {"form": form, "files": user_files}
            return render(request, self.template_name, context)
