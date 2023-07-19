from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_view, name="entry_view"),
    path("search/", views.search_view, name="search_view"),
    path("new_page/", views.new_page_view, name="new_page_view"),
    path("wiki/<str:title>/edit", views.edit_page_view, name="edit_page_view"),
    path("random_page/", views.random_page_view, name="random_page_view"),
]
