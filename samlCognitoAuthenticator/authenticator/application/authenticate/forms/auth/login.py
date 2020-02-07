from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class AuthLoginForm(AuthenticationForm):

    # overriding clean method to change default authentication behaviour
    def clean(self):
        userid = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if userid and password:
            self.user_cache = authenticate(
                username=userid,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

