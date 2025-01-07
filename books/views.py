
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views import View
from django.contrib import messages
from core.utils import send_mail_to_user
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from .models import Book, BorrowedBook, Reviews
# Create your views here.


class BookDetails(DetailView):
    template_name = 'books/book_details.html'
    model = Book
    slug_field = 'slug'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        book = Book.objects.get(slug=slug)
        user = self.request.user
        canReview = False
        if user.is_authenticated:
            canReview = BorrowedBook.objects.filter(
                user=user, book=book).exists()
        context["related_books"] = Book.objects.all()[0:5]
        context['form'] = ReviewForm
        context['canReview'] = canReview
        context['reviews'] = Reviews.objects.filter(
            book=book).order_by('-rating')
        return context

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        if form.is_valid():
            book = self.get_object()
            user = self.request.user
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
            Reviews.objects.create(user=user, book=book,
                                   rating=rating, review=review)
            messages.success(
                self.request, f"Review posted !!")
        return self.get(request, slug=slug)


class BorrowBook(LoginRequiredMixin, View):
    def post(self, request, slug):
        book = Book.objects.get(slug=slug)
        user = request.user
        user_account = request.user.user_account
        book_price = book.price

        isAvailable = BorrowedBook.objects.filter(
            user=user, book=book).exists()

        if isAvailable:
            messages.success(
                self.request, f"Already borrowed this book!!")
        elif user_account.balance < book_price:
            messages.success(
                self.request, f"not enough balance to borrow this book")
        else:
            user_account.balance -= book_price
            user_account.save(update_fields=['balance'])

            BorrowedBook.objects.create(user=user, book=book)

            messages.success(
                self.request, f"Successfully borrowed this book")
            send_mail_to_user("Book borrowed notification", self.request.user, 'books/borrow_book_email.html', {
                'user': self.request.user,
                'book': book
            })
        return redirect("book_details", slug=slug)
