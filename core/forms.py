# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

User = get_user_model()


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="We'll use this for confirmations."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # password fields come from the base class; include username + email
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    """
    Accept either username OR email in the username field.
    Authenticate manually (no super().clean() first) so can try both paths.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the label + placeholder to show Username Or Email
        self.fields["username"].label = "Username or Email"
        self.fields["username"].widget.attrs.update(
            {"placeholder": "username or email"}
        )

    def clean(self):
        username_or_email = (self.data.get("username") or "").strip()
        password = self.data.get("password")

        if not username_or_email or not password:
            raise forms.ValidationError(
                self.error_messages["invalid_login"], code="invalid_login"
            )

        user = authenticate(self.request, username=username_or_email, password=password)

        if user is None and "@" in username_or_email and "." in username_or_email:
            # Try resolving email -> username, then authenticate again
            try:
                u = User.objects.get(email__iexact=username_or_email)
                user = authenticate(
                    self.request, username=u.username, password=password
                )
            except User.DoesNotExist:
                pass  # keep user as None

        if user is None:
            raise forms.ValidationError(
                self.error_messages["invalid_login"], code="invalid_login"
            )

        # Let Django run its standard account checks
        self.confirm_login_allowed(user)
        self.user_cache = user
        return {"username": username_or_email, "password": password}
