# Este arquivo agora importa as views modularizadas
from .views.project_views import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectDetailView,
)
from .views.comment_views import add_comment, delete_comment
from .views.attachment_views import add_attachment, delete_attachment


