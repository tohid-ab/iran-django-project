from .models import Comment, ContactUs
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name', 'title', 'email', 'comment')