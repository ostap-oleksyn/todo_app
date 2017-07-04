from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, CharField, Form, PasswordInput, BooleanField, CheckboxInput

from todo.models import Task


def profanity(value):
    if 'fuck' in value:
        raise ValidationError('Text contains profanity')


class CreateTaskForm(ModelForm):
    text = CharField(label='', widget=TextInput(attrs={'placeholder': 'New Task'}), validators=[profanity])

    class Meta:
        model = Task
        exclude = ['user', 'done']


class EditTaskForm(ModelForm):
    text = CharField(validators=[profanity])

    class Meta:
        model = Task
        exclude = ['user']


class LoginForm(Form):
    username = CharField(min_length=3, max_length=15, widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(min_length=8, max_length=15, widget=PasswordInput(attrs={'placeholder': 'Password'}))
    remember_me = BooleanField(widget=CheckboxInput(attrs={'label': 'Remember Me'}), required=False)
