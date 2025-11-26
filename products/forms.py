from django import forms
from models_app.models import Review

class Reviewform(forms.ModelForm):
    RATING_CHOICES=[
        (1,'★'),
        (2,'★★'),
        (3,'★★★'),
        (4,'★★★★'),
        (5,'★★★★★'),
    ]
    rating=forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(attrs={'class': 'rating-stars'}),label='Rating: ')
    class Meta:
        model=Review
        fields=['title','comment','rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter a review title',
                'class': 'form-control',
                'style': 'font-size: 1.2rem; padding: 0.75rem; width:50%',
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Share your experience',
                'class': 'form-control',
                'rows': 4,
                'style': 'font-size: 1.2rem; padding: 0.75rem; width: 80%; height: 150px',
            })
        }