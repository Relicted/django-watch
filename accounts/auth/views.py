import secrets

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, logout
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.views.generic import FormView
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
# ====== #
from accounts.auth.tokens import activation_token
from accounts.models import PasswordResetLink
from .forms import (
    CustomRegistrationForm,
    CustomAuthenticationForm,
    ResetPasswordEmailForm,
    ResetPasswordForm
                    )


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse(form.errors)
        else:
            return super(CustomLoginView, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            data = {
                'reload': True
            }
            return JsonResponse(data)
        return super(CustomLoginView, self).form_valid(form)

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
        return reverse('account:registration')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        email = instance.email
        user = instance.username
        messages.success(
            self.request,
            _(f'{user} created, activation instructions were sent to {email}')
        )

        self.send_email(instance)
        return super(CustomRegistrationView, self).form_valid(form)

    def send_email(self, user):
        site = get_current_site(self.request)
        subject = _('Activation instructions.')
        message = render_to_string('accounts/reg_confirm_email.html', {
            'user': user,
            'domain': site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': activation_token.make_token(user),
        })

        user.email_user(subject, message, html_message=message)


def activate(request, uidb64, token):
    error = _('Activation error: ')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        error += _('Unknown user')

    if not activation_token.check_token(user, token):
        error += _('Token invalid or expired!')

    if user and (user.is_active and user.profile.email_confirmed):
        error += _('User already activated')
        messages.error(request, error)
        return render(request, 'accounts/activation.html')

    if user and activation_token.check_token(user, token):
        user.profile.email_confirmed = True
        user.save()

        login(request, user)
        messages.success(request, _('Activated! Please, fill in your profile!'))
        return redirect('settings:profile')

    else:
        messages.error(request, error)
        return render(request, 'accounts/activation.html')


def password_reset(request):
    form = ResetPasswordEmailForm()
    if request.method == "POST":
        form = ResetPasswordEmailForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.get(email__iexact=email)
            site = get_current_site(request)
            subject = _('Password reset instructions.')

            token = PasswordResetLink.objects.create(
                user=user,
                code=secrets.token_hex(88)
            )

            message = render_to_string('accounts/pass_reset_email.html', {
                'user': user,
                'domain': site,
                'token': token.code,
            })

            user.email_user(subject, message)
            messages.success(
                request,
                _('Password reset instructions were sent to your email.'))
            return redirect('account:password_reset')
        else:
            return render(request,
                          'accounts/password_reset.html',
                          locals())
    return render(request,
                  'accounts/password_reset.html',
                  locals())


def complete_reset(request, token):
    try:
        uid = PasswordResetLink.objects.get(code=token)
        user = uid.user
        if not uid.code_valid():
            raise ValueError('Expired Link')
    except (PasswordResetLink.DoesNotExist, ValueError):

        messages.error(request, _('chet ne ok'))
        return redirect('account:password_reset')

    form = ResetPasswordForm(user)
    if request.method == "POST":
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            uid.delete()
            messages.success(request, _('New password set successfully.'))
            return redirect('account:login')
        else:
            return render(request,
                          'accounts/password_reset_complete.html',
                          {'form': form})
    return render(request,
                  'accounts/password_reset_complete.html',
                  {'form': form})
