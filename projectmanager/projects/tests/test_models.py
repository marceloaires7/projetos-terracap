from django.test import TestCase
from ..models import Project, ProjectComment, ProjectAttachment
from django.contrib.auth import get_user_model
from djmoney.money import Money

User = get_user_model()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(
            name="Projeto Teste",
            lider="Líder Teste",
            GPP=True,
            prioridade="Alta",
            remuneracao=Money(1000, 'BRL'),
            data_inicio='2023-01-01'
        )

    def test_project_creation(self):
        self.assertEqual(self.project.name, "Projeto Teste")
        self.assertEqual(self.project.lider, "Líder Teste")
        self.assertTrue(self.project.GPP)
        self.assertEqual(self.project.prioridade, "Alta")
        self.assertEqual(self.project.remuneracao, Money(1000, 'BRL'))
        self.assertEqual(str(self.project), "Projeto Teste")

class ProjectCommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(
            name="Projeto Teste",
            lider="Líder Teste",
            data_inicio='2023-01-01'
        )
        self.comment = ProjectComment.objects.create(
            project=self.project,
            user=self.user,
            comment_text="Este é um comentário de teste."
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.project, self.project)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.comment_text, "Este é um comentário de teste.")
        self.assertIsNotNone(self.comment.criado_em)

class ProjectAttachmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.project = Project.objects.create(
            name="Projeto Teste",
            lider="Líder Teste",
            data_inicio='2023-01-01'
        )
        self.attachment = ProjectAttachment.objects.create(
            project=self.project,
            user=self.user,
            file_name="documento.pdf",
            file_path="uploads/documento.pdf"
        )

    def test_attachment_creation(self):
        self.assertEqual(self.attachment.project, self.project)
        self.assertEqual(self.attachment.user, self.user)
        self.assertEqual(self.attachment.file_name, "documento.pdf")
        self.assertEqual(self.attachment.file_path, "uploads/documento.pdf")
        self.assertIsNotNone(self.attachment.criado_em)


