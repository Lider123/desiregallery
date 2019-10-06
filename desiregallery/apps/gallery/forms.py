from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("comment_text",)
        labels = {
            "comment_text": "",
        }
        widgets = {
            "comment_text": forms.TextInput(attrs={
                "placeholder": "Add a comment",
                "id": "comment-input",
            }),
        }
