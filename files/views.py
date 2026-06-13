from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import CreateFolderForm, FileUploadForm
from .models import Folder


class HomeView(LoginRequiredMixin, View):
    template_name = "files/home.html"
    login_url = "users:login"
    redirect_field_name = "next"

    def get(self, request, current_path: str):
        folder, created = Folder.objects.get_or_create(
            user=request.user, full_path=current_path
        )

        if created:
            messages.info(request, f"Создана новая папка: {current_path}")

        form = FileUploadForm()
        folder_form = CreateFolderForm()

        context = {
            "form": form,
            "folder_form": folder_form,
            "current_path": current_path,
            "folder": folder,
        }
        return render(request, self.template_name, context)

    def post(self, request, current_path: str):
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                folder = get_object_or_404(
                    Folder, user=request.user, full_path=current_path
                )

                folder_obj = form.save(commit=False)
                folder_obj.user = request.user
                folder_obj.name = request.FILES["file"].name
                folder_obj.folder = folder
                folder_obj.file.field.upload_to = f"{current_path}/"
                folder_obj.save()

                messages.success(request, f"Файл {folder_obj.name} успешно загружен")
            except Folder.DoesNotExist:
                messages.error(request, "Папка не найдена")
            except Exception as e:
                messages.error(request, f"Ошибка загрузки: {e}")
        else:
            messages.error(request, "Ошибка валидации формы")

        return redirect("files:home", current_path=current_path)


class FolderCreateView(LoginRequiredMixin, View):
    login_url = "users:login"
    redirect_field_name = "next"

    def post(self, request, current_path: str):
        form = CreateFolderForm(request.POST)

        if form.is_valid():
            folder_name = form.cleaned_data["name"]

            try:
                parent_folder = Folder.objects.get(
                    user=request.user, full_path=current_path
                )
            except Folder.DoesNotExist:
                messages.error(request, "Родительская папка не найдена")
                return redirect("files:home", current_path=current_path)

            folder_exists = Folder.objects.filter(
                user=request.user, name=folder_name, parent=parent_folder
            ).exists()

            if folder_exists:
                messages.error(request, "Папка с таким именем уже существует")
            else:
                try:
                    folder_obj = form.save(commit=False)
                    folder_obj.user = request.user
                    folder_obj.name = folder_name
                    folder_obj.parent = parent_folder
                    folder_obj.save()

                    messages.success(request, f"Папка '{folder_name}' успешно создана")
                except Exception as e:
                    messages.error(request, f"Ошибка создания папки: {e}")
        else:
            messages.error(request, "Ошибка: название папки обязательно")

        return redirect("files:home", current_path=current_path)
