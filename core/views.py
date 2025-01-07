from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book, Category
# Create your views here.


class HomePageView(ListView):
    template_name = 'core/homepage.html'
    model = Book
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category')

        if category is not None:
            queryset = Book.objects.filter(
                category__slug=category).order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context