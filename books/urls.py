from django.urls import path
from .views import BookDetails, BorrowBook

urlpatterns = [
    path('detail/<slug:slug>/', BookDetails.as_view(), name="book_details"),
    path('borrow/<slug:slug>/', BorrowBook.as_view(), name="borrow_book"),
]