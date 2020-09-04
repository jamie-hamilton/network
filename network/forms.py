from django import forms
from django.forms import CharField, ModelForm

from .models import User, Post


class PostForm(forms.ModelForm):
    post = forms.CharField(
                max_length=180,
                label='',
                widget=forms.Textarea(
                    attrs={
                        "placeholder": "Shout into the abyss...",
                        "class": "form-control post-field",
                        "rows": 2,
                    }
                )
            )

    class Meta:
        model = Post
        fields = ['post',]


class UploadPhotoForm(forms.ModelForm):
    profile_image = forms.ImageField(
                label="",
                widget=forms.FileInput(
                    attrs={
                        "class": "form-control-file",
                        "id": "image-file",
                    })
                )

    class Meta:
        model = User
        fields = ['profile_image',]