from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account


class RegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=2049)
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email', 'address']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            address = self.cleaned_data.get('address')
            Account.objects.create(user=our_user, address=address)
        return our_user


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs={'id': 'required'}))
    address = forms.CharField(max_length=2049)


class DepositForm(forms.Form):
    amount = forms.IntegerField(
        max_value=1000000, min_value=1000, help_text="Enter the amount you want to deposit")

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount < 1000:
            raise forms.ValidationError(f"Minimum deposit amount is 1000")
        elif amount > 1000000:
            raise forms.ValidationError("Maximum deposit amount is 1000000")

        return amount