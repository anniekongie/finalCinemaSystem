from django.forms import ModelForm, Textarea
from movies.models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15})
        }



