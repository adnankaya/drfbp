from django.contrib.auth import get_user_model
from django.db.models import Q
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


User = get_user_model()


class UserLoginForm(forms.Form):
    query = forms.CharField(label=_('Email or Username or Password'))
    password = forms.CharField(label='Parola', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')

        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(phone__iexact=query) |
            Q(email__iexact=query)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError(_('User does not exist!'))
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError(_('Password is incorrect!'))
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone','first_name')
