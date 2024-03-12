from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Post, Response


class PostForm(ModelForm):      # форма для создания поста
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        title = cleaned_data.get('title')

        if title == content:
            raise ValidationError('Название и текст не должны совпадать')

        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        labels = {'content': 'Содержимое отклика'}
