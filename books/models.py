from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(
        max_length=2000, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name+"-"+str(self.id))
        return super().save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    category = models.ManyToManyField(
        Category)
    image = models.ImageField(upload_to="book_images/")
    slug = models.SlugField(
        max_length=2000, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name+"-"+str(self.id))
        return super().save(*args, **kwargs)


class Reviews(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_review")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_review")
    review = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.book.name} - {self.user.username}"


STATUS_CHOICES = [
    ('borrowed', 'borrowed'),
    ('returned', 'returned'),
]


class BorrowedBook(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="borrowed")

    def __str__(self) -> str:
        return f"{self.user.username}"