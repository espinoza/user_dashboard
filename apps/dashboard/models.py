from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):

    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    level = models.IntegerField()

    first_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Too short first name"
            )
        ]
    )

    last_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(
                limit_value=2,
                message="Too short last name"
            )
        ]
    )
    description = models.CharField(max_length=10000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):

    content = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="messages")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):

    content = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="comments")
    message = models.ForeignKey(Message, on_delete=models.CASCADE,
                                related_name="comments")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
