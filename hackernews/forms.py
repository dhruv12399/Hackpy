from django.forms import ModelForm

from .models import Link,Comments
from django import forms


class LinkForm(ModelForm):
	class Meta:
		model = Link
		fields = ['title', 'url']

class CommentForm(ModelForm):
	content = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = Comments
		fields = ['content']


class SearchForm(forms.Form):
   search = forms.CharField(max_length = 50)
   