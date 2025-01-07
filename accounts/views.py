from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import send_mail_to_user
from books.models import BorrowedBook
from django.views import View
from books.models import Book
import datetime
from .forms import RegistrationForm, DepositForm, UpdateUserForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
# Create your views here.


class UpdateUserInfo(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'address': user.user_account.address,
        }
        form = UpdateUserForm(
            initial=initial
        )
        return render(request, 'accounts/form.html', {
            'form': form,
            'type': "Update"
        })

    def post(self, request, *args, **kwargs):
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']

            user = self.request.user
            user_account = user.user_account
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save(update_fields=['first_name', 'last_name', 'email'])

            user_account.address = address
            user_account.save(update_fields=['address'])
            messages.success(self.request, "Updated your information")
        return redirect("profile")


class UserRegistrationForm(FormView):
    form_class = RegistrationForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy("home_page")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user=user)
        messages.success(self.request, "Registration successfully completed")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Registration"
        return context


class UserLoginForm(LoginView):
    template_name = 'accounts/form.html'
    next_page = reverse_lazy("home_page")
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Logged in successful")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login"
        return context


class UserLogout(LogoutView):
    next_page = reverse_lazy("home_page")


class DepositMoney(LoginRequiredMixin, FormView, ):
    template_name = 'accounts/form.html'
    success_url = reverse_lazy("home_page")
    form_class = DepositForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Deposit"
        return context

    def form_valid(self, form):
        amount = form.cleaned_data["amount"]

        user = self.request.user
        user_account = user.user_account
        user_account.balance += amount
        user_account.save(update_fields=['balance'])

        messages.success(self.request, f"{amount}tk deposited to your account")
        send_mail_to_user("Deposit", user, 'accounts/deposit_mail.html', {
            'user': user,
            'amount': amount,
            'current_time': datetime.datetime.now()
        })

        return super().form_valid(form)


class UserProfile(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    model = BorrowedBook
    context_object_name = 'borrowed_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = BorrowedBook.objects.filter(
            user=self.request.user).order_by('timestamp')
        return queryset


class ReturnBorrowedBook(LoginRequiredMixin, View):
    def post(self, request, slug):
        book = Book.objects.get(slug=slug)
        user = self.request.user
        user_account = user.user_account

        user_account.balance += book.price
        user_account.save(update_fields=['balance'])

        borrowed_book = BorrowedBook.objects.get(user=user, book=book)
        borrowed_book.status = 'returned'
        borrowed_book.save(update_fields=['status'])

        messages.success(self.request, f"{book.name} is returned")
        send_mail_to_user("Returned a book", user, 'accounts/return_book_mail.html', {
            'username': user.username,
            'bookname': book.name,
            'price': book.price,
            'time': datetime.datetime.now()
        })

        return redirect("profile")


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/form.html'
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Change Password"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Password has been changed")
        return super().form_valid(form)