from django.forms import ModelForm
from .models import *

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_done', 'performer_id', 'tags']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

