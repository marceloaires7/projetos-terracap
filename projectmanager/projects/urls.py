# Django imports
from django.urls import path

# Local imports
from .views.project_views import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectDetailView,
)
from .views.comment_views import add_comment, delete_comment
from .views.attachment_views import add_attachment, delete_attachment

app_name = "projects"  # Namespace para as URLs do app

urlpatterns = [
    path("", ProjectListView.as_view(), name="list"),
    path("new/", ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="delete"),
    path("<int:pk>/add_comment/", add_comment, name="add_comment"),
    path("<int:pk>/add_attachment/", add_attachment, name="add_attachment"),
    path(
        "<int:project_id>/delete_comment/<int:comment_id>/",
        delete_comment,
        name="delete_comment",
    ),
    path(
        "<int:project_id>/delete_attachment/<int:attachment_id>/",
        delete_attachment,
        name="delete_attachment",
    ),
]


