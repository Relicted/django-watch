from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# =====
from .forms import (ProfileForm,
                    PictureForm,
                    CustomPasswordChangeForm)


def profile_view(request, profile):
    instance = get_object_or_404(User, username__iexact=profile)
    return render(request, 'accounts/profile_detail.html', locals())


@login_required
def profile(request):
    instance = request.user.profile
    form = ProfileForm(instance=instance)
    picture = PictureForm()
    if request.method == 'POST' and not request.FILES:
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('settings:profile')
        else:
            return render(request,
                          'accounts/settings.html',
                          locals())

    elif request.method == 'POST' and request.FILES:
        picture = PictureForm(request.POST, request.FILES)
        if picture.is_valid():
            instance.picture = request.FILES.get('picture')
            instance.save(update_fields=['picture'])
            return redirect('settings:profile')
        else:
            print(picture.errors)
            return render(request,
                          'accounts/settings.html',
                          locals())
    else:
        return render(request,
                      'accounts/settings.html',
                      locals())


@login_required
def account(request):
    instance = request.user
    form = CustomPasswordChangeForm(request.user)
    hide_label = True
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password updated')
            return redirect('settings:account')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request,
                          'accounts/settings.html',
                          locals())
    else:
        return render(request,
                      'accounts/settings.html',
                      locals())
