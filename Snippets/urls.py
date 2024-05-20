from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="snippets-home"),
    path('snippets/add', views.add_snippet_page, name="snippets-add"),
    path('snippets/list', views.snippets_page, name="snippets-list"),
    path('snippets/<int:snippet_id>/', views.get_snippet, name="snippet-detail"),
    #path('snippets/create', views.create_snippet, name="create-snippet"),
    path('snippets/<int:snippet_id>/delete', views.delete_snippet, name="delete-snippet"),
    path('snippets/<int:snippet_id>/change', views.change_snippet, name="change-snippet"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
