from django import forms
from . import models



class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'textarea-field',
                'placeholder': 'Write your content here',
                'rows': 10
            }),
        }
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment...',
                'rows': 3
            })
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply...',
                'rows': 2
            })
        }
class SearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search posts...'
        }),
        required=False
    )