from django import forms
from .models import Post, Comment
from .validators import validate_image_file_extension, validate_image_file_size

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=60)
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False, validators=[validate_image_file_extension, validate_image_file_size], label='Image')

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        if commit:
            comment.save()
        return comment