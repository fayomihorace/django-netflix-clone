from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    """Registration form class."""

    firstname = forms.CharField(label="First name")
    lastname = forms.CharField(label="Last name")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=True),
        min_length=6,
        max_length=20
    )
    password_conf = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    def clean(self):
        """Check if the form is validated."""
        # perform default validation of the form
        super(RegisterForm, self).clean()

        # extract user input data
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        # Check if the password match the password confirmation
        if password != password_conf:
            self._errors['password_conf'] = self.error_class([
                "wrong confirmation"
            ])

        # Check if the email used doen't already exist
        if User.objects.filter(username=email).exists():
            self._errors['email'] = self.error_class(['Email already exist'])

        # return any errors if found
        return self.cleaned_data


class LoginForm(forms.Form):
    """Login form class."""

    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class SearchForm(forms.Form):
    """Search form class."""
    search_text = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search'})
    )
