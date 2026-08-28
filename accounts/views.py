from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from .models import Profile
from quiz.models import QuizAttempt


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        # Let super handle login
        response = super().form_valid(form)
        if remember_me:
            # 2 weeks
            self.request.session.set_expiry(1209600)
        else:
            # Browser close
            self.request.session.set_expiry(0)
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return response

    def form_invalid(self, form):
        # Ensure non-field errors are shown as friendly message
        # AuthenticationForm already adds error: "Please enter a correct username and password..."
        # We keep it, but ensure it is human-friendly
        return super().form_invalid(form)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("/dashboard/")
        else:
            # Add a friendly non-field message if there are errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    profile = request.user.profile
    attempts = QuizAttempt.objects.filter(user=request.user).order_by("-started_at")[:10]
    total_attempts = QuizAttempt.objects.filter(user=request.user, status="COMPLETED").count()
    from django.db.models import Avg
    avg_score = QuizAttempt.objects.filter(user=request.user, status="COMPLETED").aggregate(avg=Avg("score"))["avg"] or 0
    return render(request, "accounts/profile.html", {"profile": profile, "attempts": attempts, "total_attempts": total_attempts, "avg_score": avg_score})


@login_required
def profile_edit(request):
    if request.method == "POST":
        bio = request.POST.get("bio","")
        lang = request.POST.get("language","en")
        dark = request.POST.get("dark_mode") == "on"
        profile = request.user.profile
        profile.bio = bio
        profile.language = lang
        profile.dark_mode = dark
        profile.save()
        messages.success(request, "Profile updated")
        return redirect("/accounts/profile/")
    return render(request, "accounts/profile_edit.html", {"profile": request.user.profile})
