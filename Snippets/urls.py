from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="snippets-home"),
    path('snippets/add', views.add_snippet_page, name="snippets-add"),
    path('snippets/list', views.snippets_page, name="snippets-list"),
    path('snippets/my_list', views.my_snippets_page, name="my-snippets"),
    path('snippets/<int:snippet_id>/', views.get_snippet, name="snippet-detail"),
    #path('snippets/create', views.create_snippet, name="create-snippet"),
    path('snippets/<int:snippet_id>/delete', views.delete_snippet, name="delete-snippet"),
    path('snippets/<int:snippet_id>/edit', views.snippet_edit, name='snippet-edit'),
    path('snippets/<int:snippet_id>/change', views.change_snippet, name="change-snippet"),
    path('snippets/<int:id>/<str:name>/<str:lang>/<str:code>/save', views.save_snippet, name="save-snippet"),
    path('login_form', views.login_form, name="login-form"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
