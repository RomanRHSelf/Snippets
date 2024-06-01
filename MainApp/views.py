from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserForm
from django.contrib import auth

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

def snippets_page(request):
    snippets_from_db = Snippet.objects.filter(private=True) #all()
    context = {'pagename': 'Просмотр сниппетов',
               "snippets_list": snippets_from_db,
               }    
    return render(request, 'pages/view_snippets.html', context)

def my_snippets_page(request):
    try:
        my_snippets_from_db = Snippet.objects.filter(user=request.user)
        context = {'pagename': 'Просмотр моих сниппетов',
                   "snippets_list": my_snippets_from_db,
                   }    
    except TypeError as te:
        return HttpResponse('Список не возможно определить. Вернитесь на <a href="{% url "snippets-list" %}">главную страницу</a> и авторизуйтесь')
    return render(request, 'pages/view_snippets.html', context)

def get_snippet(request, snippet_id:int):
    try:
        snippet_from_db = Snippet.objects.get(id=snippet_id)
        context = {
            "pagename": 'Детализация сниппета',
            "snippet": snippet_from_db
        }
        return render(request=request, template_name="pages/view_snippet_detail.html", context=context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Товар {snippet_id} не найден')
    
def change_snippet(request, snippet_id:int):
    try:
        #  if request.method == "PUT":
        # form = SnippetForm() # request.PUT
        snippet_from_db = Snippet.objects.get(id=snippet_id)
        context = {
            "pagename": 'Редактирование сниппета',
            "snippet": snippet_from_db,
            #"form": form
        }
        return render(request=request, template_name="pages/snippet_change.html", context=context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Товар {snippet_id} не найден')

def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                'form': form
                }
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
        form = SnippetForm(request.POST)    
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")
        return render(request, "pages/add_snippet.html", {'form': form})

def snippet_edit(request, snippet_id: int):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404
    
    # Variant 1
    # Хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {
            "pagename": "Редактирование сниппета",
            "snippet": snippet,
            "type": "edit"
        }
        return render(request, "pages/snippet_detail.html", context)
    
    # Variant 2
    # ==================================================================
    # Получение сниппета с помощью формы SnippetForm
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request, "pages/add_snippet.html", {"form": form})
    # ==================================================================

    # Хотим использовать данные из формы и сохранить изменения в базе
    if request.method == "POST":
        data_form = request.POST
        # Есть экземпляр класса Snippet и новые данные в словаре data_form 
        # что нужно: взять данные из data_form и заменить ими значения атрибутов экземпляра snippet
        # как это сделать?
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.private = data_form["private"]
        if (change_date := data_form.get("creation_date")):
            snippet.creation_date = change_date
        # сохраняем этот изменения в базу
        snippet.save()
        return redirect("snippets-list")


#def create_snippet(request):
 #   if request.method == "POST":
  #      form = SnippetForm(request.POST)    
   #     if form.is_valid():
    #        form.save()
     #       return redirect("snippets-list")
      #  return render(request, "pages/add_snippet.html", {'form': form})

def delete_snippet(request, snippet_id:int):
    snippet_for_delete = Snippet.objects.get(id=snippet_id)
    snippet_for_delete.delete()
    return redirect("snippets-list")

def save_snippet(request, id:int, name: str, lang: str, code: str):
    snippet_for_save = Snippet.objects.get(id=id)
    snippet_for_save.name = name
    snippet_for_save.lang = lang
    snippet_for_save.code = code
    snippet_for_save.save()
    return redirect("snippets-list")
    t = """
    if request.method == "PUT":
        form = SnippetForm(request.POST)    
        if form.is_valid():
            form.save()
            return redirect("snippets-list")
        return render(request, "pages/snippet_change.html", {'form': form})
        """

def login_form(request):
    #return HttpResponseNotFound(f'Будущая форма регистрации')
    #return render(request, "pages/login_form.html")  # а вот так  -- redirect("login-form") -- получаю ошибку 127.0.0.1 redirected you too many times. 
    if request.method == "GET":
        form = UserForm()
        context = {'pagename': 'Регистрация нового пользователя',
                'form': form
                }
        return render(request, 'pages/login_form.html', context)

    if request.method == "POST":
        form = UserForm(request.POST)    
        try:
            if form.is_valid():
                user = form.save(commit=False)
                # пользователь на этом этапе ещё не может быть авторизован if request.user.is_authenticated:
                #                                                              snippet.user = request.user
                user.save()
                return redirect("") #snippets-list
        except Exception as e:
            return HttpResponse(f'Ошибка авторизации {e} <a href="/login_form">назад</a>')
        # return render(request, "pages/login_form.html", {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username =", username)
        print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            #error msg
            context = {
                "pagename": "PythonBin",
                "errors": ["wrong username or password"]
            }
            return render(request, "pages/index.html", context)
    return redirect("snippets-home") #HttpResponse('check')


def logout(request):
    auth.logout(request)
    return redirect('snippets-home')