# Django imports
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test

# Local imports
from ..models import Project, ProjectAttachment
from ..forms import ProjectAttachmentForm


@login_required
def add_attachment(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.project = project
            attachment.user = request.user
            attachment.save()
    attachments = project.attachments.order_by("-criado_em")
    html = render_to_string(
        "projects/partials/attachments_list.html",
        {"attachments": attachments, "project": project, "user": request.user},
    )
    return HttpResponse(html)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_attachment(request, project_id, attachment_id):
    attachment = get_object_or_404(ProjectAttachment, id=attachment_id, project_id=project_id)
    project = get_object_or_404(Project, id=project_id)
    attachment.delete()
    attachments = project.attachments.order_by("-criado_em")
    return render_to_string(
        request,
        "projects/partials/attachments_list.html",
        {"attachments": attachments, "project": project, "user": request.user},
    )


