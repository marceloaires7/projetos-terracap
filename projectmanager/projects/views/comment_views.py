# Django imports
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test

# Local imports
from ..models import Project, ProjectComment
from ..forms import ProjectCommentForm


@login_required
def add_comment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
    comments = project.comments.select_related("user").order_by("-criado_em")
    html = render_to_string(
        "projects/partials/comments_list.html",
        {"comments": comments, "project": project, "user": request.user},
    )
    return HttpResponse(html)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_comment(request, project_id, comment_id):
    comment = get_object_or_404(ProjectComment, id=comment_id, project_id=project_id)
    project = get_object_or_404(Project, id=project_id)
    comment.delete()
    comments = project.comments.select_related("user").order_by("-criado_em")
    return render_to_string(
        request,
        "projects/partials/comments_list.html",
        {"comments": comments, "project": project, "user": request.user},
    )


