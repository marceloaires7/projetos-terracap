import django_filters
from .models import Project


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Nome do Projeto")
    lider = django_filters.ChoiceFilter(
        label="Líder do Projeto",
        choices=lambda: [
            (lider, lider)
            for lider in Project.objects.order_by("lider")
            .values_list("lider", flat=True)
            .distinct()
            if lider
        ],
    )

    class Meta:
        model = Project
        fields = ["name", "lider", "prioridade", "ciclo", "GPP", "mapRisk"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preservar parâmetros de ordenação nos filtros
        order_by = self.data.get("order_by")
        direction = self.data.get("direction")

        if order_by and direction:
            self.form.initial["order_by"] = order_by
            self.form.initial["direction"] = direction
