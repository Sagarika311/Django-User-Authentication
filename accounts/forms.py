from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if not p1 or not p2:
            raise forms.ValidationError('Please confirm your password')
        if p1 != p2:
            raise forms.ValidationError('Passwords do not match')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username / Email / Phone')
    remember_me = forms.BooleanField(required=False, initial=False)

class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomPasswordChangeForm(PasswordChangeForm):
    # uses Django built-in PasswordChangeForm behaviour; we can extend if needed
    pass
