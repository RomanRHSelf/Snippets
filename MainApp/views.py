from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from MainApp.models import Snippet
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            form.save()
            return redirect("snippets-list")
        return render(request, "pages/add_snippet.html", {'form': form})

def snippets_page(request):
    snippets_from_db = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов',
               "snippets_list": snippets_from_db,
               }    
    return render(request, 'pages/view_snippets.html', context)


def get_snippet(request, snippet_id:int):
    try:
        snippet_from_db = Snippet.objects.get(id=snippet_id)
        context = {
            "pagename": 'Детализация сниппета',
            "snippet_id": snippet_from_db.id,
            "name": snippet_from_db.name,
            "code": snippet_from_db.code,
            "lang": snippet_from_db.lang,
            "creation_date": snippet_from_db.creation_date
        }
        return render(request=request, template_name="pages/view_snippet_detail.html", context=context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f'Товар {snippet_id} не найден')
    
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