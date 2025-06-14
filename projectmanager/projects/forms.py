from django import forms
from django.core.exceptions import ValidationError
from .models import Project, ProjectComment, ProjectAttachment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "data_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",  # Opcional: classe para estilização
                },
            ),
            "entrega": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
            ),
            "descricao": forms.Textarea(attrs={"rows": 3}),
            "situacao": forms.Textarea(attrs={"rows": 3}),
            "meta": forms.Textarea(attrs={"rows": 3}),
        }

    # Adicione este método para inicializar os campos de data corretamente
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Formata as datas existentes para o formato YYYY-MM-DD
        if self.instance and self.instance.data_inicio:
            self.initial["data_inicio"] = self.instance.data_inicio.strftime("%Y-%m-%d")

        if self.instance and self.instance.entrega:
            self.initial["entrega"] = self.instance.entrega.strftime("%Y-%m-%d")

    def clean_latitude(self):
        latitude = self.cleaned_data.get("latitude")
        if latitude is not None and not (-90 <= latitude <= 90):
            raise ValidationError("Latitude deve estar entre -90 e 90 graus.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get("longitude")
        if longitude is not None and not (-180 <= longitude <= 180):
            raise ValidationError("Longitude deve estar entre -180 e 180 graus.")
        return longitude

    def clean_area(self):
        area = self.cleaned_data.get("area")
        if area is not None and area < 0:
            raise ValidationError("Área do terreno não pode ser negativa.")
        return area

    def clean_progressoPlan(self):
        progresso = self.cleaned_data.get("progressoPlan")
        if progresso is not None and not (0 <= progresso <= 100):
            raise ValidationError("Progresso Planejado deve estar entre 0 e 100.")
        return progresso

    def clean_progressoReal(self):
        progresso = self.cleaned_data.get("progressoReal")
        if progresso is not None and not (0 <= progresso <= 100):
            raise ValidationError("Progresso Realizado deve estar entre 0 e 100.")
        return progresso

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        entrega = cleaned_data.get("entrega")

        if data_inicio and entrega and entrega < data_inicio:
            self.add_error(
                "entrega", "Data de Entrega não pode ser anterior à Data de Início."
            )

        return cleaned_data


class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ["texto"]
        widgets = {
            "comment_text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Adicione um comentário...",
                    "class": "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                }
            )
        }

    def clean_comment_text(self):
        comment_text = self.cleaned_data.get("comment_text")
        if not comment_text or len(comment_text.strip()) == 0:
            raise ValidationError("O comentário não pode ser vazio.")
        if len(comment_text) > 500:  # Example max length
            raise ValidationError("O comentário é muito longo.")
        return comment_text


class ProjectAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = ["arquivo"]

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get("arquivo")
        if not arquivo:
            raise ValidationError("Nenhum arquivo foi selecionado.")
        # Add more file validation here if needed (e.g., file type, size)
        return arquivo
