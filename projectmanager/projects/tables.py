# projects/tables.py
import django_tables2 as tables
from .models import Project
from django.utils.html import format_html


class ProjectTable(tables.Table):
    actions = tables.Column(empty_values=(), orderable=False, verbose_name="Ações")

    def render_actions(self, record):
        return format_html(
            '<a href="/{}/edit/" class="text-blue-600 hover:text-blue-900 mr-2">Editar</a>'
            '<a href="/{}/delete/" class="text-red-600 hover:text-red-900">Excluir</a>',
            record.id,
            record.id,
        )

    def render_prioridade(self, value):
        color = {
            "Baixa": "bg-green-100 text-green-800",
            "Média": "bg-yellow-100 text-yellow-800",
            "Alta": "bg-red-100 text-red-800",
        }.get(value, "bg-gray-100 text-gray-800")
        return format_html(
            '<span class="px-2 py-1 rounded-md {}">{}</span>', color, value
        )

    def render_progressoReal(self, value):
        return format_html(
            '<div class="w-full bg-gray-200 rounded-full h-2.5">'
            '<div class="bg-blue-600 h-2.5 rounded-full" style="width: {}%"></div>'
            "</div>{}%",
            value,
            value,
        )

    class Meta:
        model = Project
        template_name = "django_tables2/tailwind.html"
        fields = (
            "name",
            "lider",
            "prioridade",
            "ciclo",
            "GPP",
            "mapRisk",
            "data_inicio",
            "entrega",
            "progressoReal",
            "actions",
        )
        attrs = {
            "class": "min-w-full divide-y divide-gray-200",
            "thead": {"class": "bg-gray-50"},
        }
