from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,UserChangeForm
from django.views.generic.edit import FormView,UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserChangeForm
from .models import User

# регистрации в системе - RegisterFormView
# входа в систему - LoginFormView
# выхода из системы - LogoutView
# просмотр профиля пользователя profile_view
# редактирование профиля пользователя UserChangeFormView
# изменение пароля - change_password


def profile_view(request):
    if request.method == 'GET':
        return render(request, 'account/profile.html')
    else:
        redirect('account:profile')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:change_pass')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {
        'form': form
    })


class UserChangeFormView(UpdateView):
    form_class = UserChangeForm
    model = User
    template_name = "account/change_user_info.html"
    success_url = reverse_lazy('account:change_user')

    def get_object(self):
        return self.request.user


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "account/login.html"

    # В случае успеха перенаправим на главную.
    success_url = reverse_lazy('account:profile')

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = reverse_lazy('account:login')

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "account/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")
