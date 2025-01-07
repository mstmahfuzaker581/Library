from .models import Reviews
from django import forms


class ReviewForm(forms.Form):
    rating = forms.IntegerField(max_value=5, min_value=1, required=True, widget=forms.NumberInput(
        attrs={'placeholder': 'Enter rating between 1 to 5'}))
    review = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'placeholder': 'Write your review here...'
    }))