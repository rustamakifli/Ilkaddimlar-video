from django import forms
from courses.models import Comment, StudentCourse


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',
        )
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Your comment',
                'class': 'form-control',
            })
        }