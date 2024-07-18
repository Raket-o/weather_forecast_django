from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic import CreateView
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "authorization/register.html"
    success_url = reverse_lazy("forecast:request_city_from_user")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("authorization:login")
