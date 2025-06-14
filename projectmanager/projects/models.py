from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from datetime import date

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Projeto")
    lider = models.CharField(max_length=200, verbose_name="Líder do Projeto")

    GPP_CHOICES = [
        (True, "Estratégico"),
        (False, "Não Estratégico"),
    ]
    GPP = models.BooleanField(choices=GPP_CHOICES, default=False, verbose_name="GPP")

    mapRisk = models.BooleanField(
        choices=[(True, "Sim"), (False, "Não")],
        default=False,
        verbose_name="Mapeamento de Risco",
    )

    PRIORIDADE_CHOICES = [
        ("Baixa", "Baixa"),
        ("Média", "Média"),
        ("Alta", "Alta"),
    ]
    prioridade = models.CharField(
        max_length=20,
        choices=PRIORIDADE_CHOICES,
        default="Baixa",
        verbose_name="Prioridade",
    )

    SEI = models.TextField(blank=True, null=True, verbose_name="Processo SEI")

    imovel = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Imóvel ou Área Definida"
    )
    latitude = models.FloatField(blank=True, null=True, verbose_name="Latitude")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Longitude")
    area = models.FloatField(blank=True, null=True, verbose_name="Área do Terreno (m²)")
    descricao = models.TextField(
        blank=True, null=True, verbose_name="Descrição do Projeto"
    )

    MODELAGEM_CHOICES = [
        ("Á definir", "Á definir"),
        ("Acordo de Cooperação Técnica", "Acordo de Cooperação Técnica"),
        ("Concessão de Direito de Superfície", "Concessão de Direito de Superfície"),
        ("Concessão de Direito Real de Uso", "Concessão de Direito Real de Uso"),
        ("Concessão de Uso de Bem Público", "Concessão de Uso de Bem Público"),
        ("Consórcio", "Consórcio"),
        ("Fundo Imobiliário", "Fundo Imobiliário"),
        ("Parceria Societária", "Parceria Societária"),
    ]
    modelagem = models.CharField(
        max_length=50,
        choices=MODELAGEM_CHOICES,
        default="Á definir",
        verbose_name="Modelagem da Proposta",
    )

    CICLO_CHOICES = [
        ("Prospecção", "Prospecção"),
        ("Formatação", "Formatação"),
        ("Fase Externa", "Fase Externa"),
        ("Gestão de Contratos", "Gestão de Contratos"),
    ]
    ciclo = models.CharField(
        max_length=20,
        choices=CICLO_CHOICES,
        default="Prospecção",
        verbose_name="Ciclo do Projeto",
    )

    situacao = models.TextField(blank=True, null=True, verbose_name="Situação Atual")

    remuneracao = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="BRL",
        blank=True,
        null=True,
        verbose_name="Remuneração Prevista (R$)",
    )

    data_inicio = models.DateField(default=date.today, verbose_name="Data de Início")
    meta = models.TextField(
        blank=True, null=True, verbose_name="Meta do Planejamento Estratégico"
    )
    entrega = models.DateField(blank=True, null=True, verbose_name="Data de Entrega")
    progressoPlan = models.FloatField(default=0, verbose_name="Progresso Planejado (%)")
    progressoReal = models.FloatField(default=0, verbose_name="Progresso Realizado (%)")
    ultimaAtt = models.DateField(
        auto_now=True, editable=False, verbose_name="Última Atualização"
    )

    def __str__(self):
        return self.name


class ProjectComment(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField("Comentário")
    criado_em = models.DateTimeField(auto_now_add=True)


class ProjectAttachment(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="attachments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to="project_attachments/")
    criado_em = models.DateTimeField(auto_now_add=True)
