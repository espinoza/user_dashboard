from django import forms
from ..models import Message, Comment


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 4})}
        labels = {"content": ""}


class CommentForm(forms.ModelForm):

    message_commented_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={"rows": 3})}
        labels = {"content": ""}


