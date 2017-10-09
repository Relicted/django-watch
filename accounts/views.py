from django.shortcuts import render, reverse
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from .forms import (
                    CustomRegistrationForm,
                    CustomAuthenticationForm,
                    )
from django.contrib.auth.views import LoginView, logout
from django.db.models import Q
from django.utils.translation import ugettext as _


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        response = super(CustomLoginView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors)
        else:
            return response

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'reload': True
            }
            return JsonResponse(data)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse("home"))
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


class CustomRegistrationView(FormView):
    form_class = CustomRegistrationForm
    template_name = 'accounts/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return super(CustomRegistrationView, self).dispatch(
            request, args, **kwargs)

    def get_success_url(self):
        return reverse('account:activation')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        super(CustomRegistrationView, self).form_valid(form)


def activation_view(request):
    return render(request, 'accounts/activation.html')