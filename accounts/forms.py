from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email or username",
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "autocomplete": "username",
            "placeholder": "Enter your email or username",
            "class": "form-control",
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "placeholder": "Enter your password",
            "class": "form-control",
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label="Remember me",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def clean_username(self):
        username_or_email = self.cleaned_data.get("username", "").strip()
        # If it looks like an email, try to resolve to username
        if "@" in username_or_email:
            try:
                user = User.objects.get(email__iexact=username_or_email)
                return user.username
            except User.DoesNotExist:
                # Leave as is; will fail authentication with friendly error
                return username_or_email
        return username_or_email

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("This account is inactive.", code="inactive")


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Full name",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your full name",
            "autocomplete": "name",
            "class": "form-control",
        })
    )
    email = forms.EmailField(
        required=True,
        label="Email address",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email address",
            "autocomplete": "email",
            "class": "form-control",
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        help_text="Letters, digits and @/./+/-/_ only. 3-30 characters.",
        widget=forms.TextInput(attrs={
            "placeholder": "Choose a username",
            "autocomplete": "username",
            "class": "form-control",
        })
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Create a strong password",
            "class": "form-control",
        }),
        help_text="Use 8+ characters with a mix of letters, numbers & symbols."
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": "Confirm your password",
            "class": "form-control",
        })
    )
    terms = forms.BooleanField(
        required=True,
        label="I agree to the Terms & Conditions and Privacy Policy",
        error_messages={"required": "You must accept the Terms & Conditions to continue."}
    )

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "password1", "password2", "terms")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters.")
        if len(username) > 30:
            raise ValidationError("Username must be 30 characters or fewer.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Try another.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists. Try logging in instead.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full_name into first_name / last_name
        full_name = self.cleaned_data.get("full_name", "").strip()
        if full_name:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.email = self.cleaned_data["email"].strip().lower()
        user.username = self.cleaned_data["username"].strip()
        if commit:
            user.save()
        return user


class ProfileForm(forms.Form):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows":3, "class":"form-control"}))
    language = forms.ChoiceField(choices=[("en","English"),("bn","Bengali")], required=False)
