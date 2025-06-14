# Django imports
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

# Third-party imports
from django_filters.views import FilterView
from django_htmx.http import trigger_client_event

# Local imports
from ..models import Project
from ..forms import ProjectForm
from ..filters import ProjectFilter


class ProjectListView(LoginRequiredMixin, FilterView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    filterset_class = ProjectFilter
    paginate_by = 999

    def get_template_names(self):
        if self.request.htmx:
            return "projects/partials/project_list_partial.html"
        return "projects/project_list.html"

    def get_queryset(self):
        # Obter parâmetro de ordenação da URL
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "asc")

        # Mapear nomes de campos para campos reais do modelo
        field_mapping = {
            "id": "id",
            "name": "name",
            "lider": "lider",
            "prioridade": "prioridade",
            "ciclo": "ciclo",
        }

        # Obter o campo real para ordenação
        order_field = field_mapping.get(order_by, "id")

        # Determinar a direção da ordenação
        if direction == "desc":
            order_field = f"-{order_field}"

        # Aplicar filtros e ordenação
        qs = super().get_queryset()
        qs = qs.order_by(order_field)

        return qs

    def get_priority_order_expression(self):
        """Ordenação simplificada por prioridade"""
        from django.db.models import F

        return F("prioridade")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adicionar informações de ordenação ao contexto
        order_by = self.request.GET.get("order_by", "id")
        direction = self.request.GET.get("direction", "asc")

        context["current_order"] = order_by
        context["current_direction"] = direction

        # Determinar a direção oposta para alternância
        context["next_direction"] = "desc" if direction == "asc" else "asc"

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            return trigger_client_event(
                response,
                "showToast",
                {"message": "Projeto criado com sucesso!", "type": "success"},
            )
        return response


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"

    def get_success_url(self):
        return reverse("projects:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # Salva o formulário e obtém o objeto atualizado
        self.object = form.save()

        if self.request.htmx:
            # Para requisições HTMX, retornamos um redirecionamento via cabeçalho
            response = HttpResponse(status=204)  # No Content
            response["HX-Redirect"] = self.get_success_url()
            return response
        else:
            # Para requisições normais, redireciona normalmente
            messages.success(self.request, "Projeto atualizado com sucesso!")
            return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            return trigger_client_event(
                response,
                "showToast",
                {"message": "Projeto excluído com sucesso!", "type": "warning"},
            )
        return response


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_queryset(self):
        # Prefetch related comments and attachments to avoid N+1 queries
        return super().get_queryset().prefetch_related("comments", "attachments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from ..forms import (
            ProjectCommentForm,
            ProjectAttachmentForm,
        )  # Import moved here to avoid circular dependency if forms are also modularized

        context["comment_form"] = ProjectCommentForm()
        context["attachment_form"] = ProjectAttachmentForm()
        return context
