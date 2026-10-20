from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegisterForm, StyledAuthenticationForm, StyledPasswordChangeForm


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to LinkHub! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = StyledAuthenticationForm


class UserLogoutView(LogoutView):
    pass


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    form_class = StyledPasswordChangeForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        messages.success(self.request, 'Password updated successfully.')
        return super().form_valid(form)


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
    return redirect('dashboard')
