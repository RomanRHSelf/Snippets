from django.forms import ModelForm, Textarea, TextInput
from MainApp.models import Snippet, User
# from django.contrib.auth.models import User

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code', 'private']
        labels = {"name": "", "lang": "", "code": ""}
        widgets = {
            "name": TextInput(attrs={"placeholder": "Название сниппета"}),
            "code": Textarea(attrs={"placeholder": "Код сниппета"})
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        # Описываем поля, которые будем заполнять в форме
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        labels = {'username': "", 'password': "", 'email': "", 'first_name': "", 'last_name': ""}
        widgets = {
            "username": TextInput(attrs={"placeholder": "логин"}),
            "password": TextInput(attrs={"placeholder": "пароль"}),
            "email": TextInput(attrs={"placeholder": "почта"}),
            "first_name": TextInput(attrs={"placeholder": "Имя"}),
            "last_name": TextInput(attrs={"placeholder": "Фамилия"})
        }