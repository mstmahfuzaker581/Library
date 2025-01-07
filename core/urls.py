from django.urls import path
from .views import HomePageView
urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('category/<slug:category>/',
         HomePageView.as_view(), name="filter_category"),
]