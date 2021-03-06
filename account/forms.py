from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class": "input", "placeholder": "رمز عبور"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class": "input", "placeholder": "تکرار رمز عبور"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": "input", "placeholder": "شماره موبایل"}),
            'first_name': forms.TextInput(attrs={"class": "input", "placeholder": "نام"}),
            'last_name': forms.TextInput(attrs={"class": "input", "placeholder": "نام خانوادگی"})
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = "09" + self.cleaned_data['username'][-9:]
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, "class": "input", "placeholder": "شماره موبایل"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', "class": "input", "placeholder": "رمز عبور"}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        username = "09" + username[-9:]
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class": "input", 'placeholder': "رمز جدید"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', "class": "input", 'placeholder': "تکرار رمز جدید"}),
    )
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,
                                          "class": "input", 'placeholder': "رمز قدیمی"}),)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {'first_name': forms.TextInput(attrs={"class": "input", 'placeholder': "نام"}),
                   'last_name': forms.TextInput(attrs={"class": "input", 'placeholder': "نام خانوادگی"}),
                   'username': forms.TextInput(attrs={"class": "input", 'placeholder': "نام حساب"}),
                   'email': forms.TextInput(attrs={"class": "input", 'placeholder': "ایمیل"}), }


class ProfileCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProfileCreateForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("user")

    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {'gender': forms.Select(attrs={"class": "input-select", 'placeholder': "جنسیت"}),
                   'user': forms.Select(attrs={"class": "input-select", 'placeholder': "حساب"}),
                   "image": forms.FileInput(attrs={"class": "input", 'placeholder': "عکس پروفایل"}),
                   "bio": forms.Textarea(attrs={"class": "input", 'placeholder': "درباره من"})}


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("user")

    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {'gender': forms.Select(attrs={"class": "input-select", 'placeholder': "جنسیت"}),
                   'user': forms.Select(attrs={"class": "input-select", 'placeholder': "حساب"}),
                   "image": forms.FileInput(attrs={"class": "input", 'placeholder': "عکس پروفایل"}),
                   "bio": forms.Textarea(attrs={"class": "input", 'placeholder': "درباره من"})}


class CompanyProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CompanyProfileForm, self).__init__(*args, **kwargs)
        if not self.request.user.is_superuser:
            self.fields.pop("user")
            self.fields.pop("confirm")

    class Meta:
        model = CompanyProfile
        fields = "__all__"
        widgets = {'bio': forms.Textarea(attrs={"class": "input", 'placeholder': 'درباه شرکت'}),
                   'user': forms.Select(attrs={"class": "input-select", 'placeholder': 'حساب'}),
                   "home_phone_number": forms.TextInput(attrs={"class": "input", 'placeholder': 'شماره تلفن'}),
                   "name": forms.TextInput(attrs={"class": "input", 'placeholder': 'نام'}),
                   "address_company": forms.Textarea(attrs={"class": "input", 'placeholder': 'آدرس'}),
                   "confirm": forms.CheckboxInput(attrs={'placeholder': 'تایید شرکت', "id": "shiping-address"}),
                   }
