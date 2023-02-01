from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import MyUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator
from .models import USERNAME_REGEX

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label="username", validators=[
        RegexValidator(
            regex=USERNAME_REGEX,
            message='Username must be alphanumeric or contain any of the following:". @ + -"',
            code='invalid_username'
        )])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        the_user = authenticate(username=username, password=password)
        if not the_user:
            raise forms.ValidationError("Invalid Credentials")

        # user_obj = User.objects.filter(username=username).first()
        # if not user_obj:
        #     raise forms.ValidationError(
        #         "Invalid Credentials -- Invalid username")
        # if not user_obj.check_password(password):
        #     raise forms.ValidationError(
        #         "Invalid Credentials -- Invalid password")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user_qs = User.objects.filter(username=username).exists()
    #     if not user_qs:
    #         raise forms.ValidationError("Invalid Credentials")
    #     return username


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff',
                  'is_active', 'is_admin')
