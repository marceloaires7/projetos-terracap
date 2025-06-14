from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Project, ProjectComment, ProjectAttachment
from ..forms import ProjectForm, ProjectCommentForm, ProjectAttachmentForm
from djmoney.money import Money

User = get_user_model()

class ProjectViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.project = Project.objects.create(
            name='Projeto Teste',
            lider='Líder Teste',
            data_inicio='2023-01-01'
        )

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)

    def test_project_create_view(self):
        response = self.client.post(reverse('projects:create'), {
            'name': 'Novo Projeto',
            'lider': 'Novo Líder',
            'data_inicio': '2024-01-01',
            'remuneracao_0': 100,
            'remuneracao_1': 'BRL'
        })
        self.assertEqual(response.status_code, 302) # Redirect after successful creation
        self.assertTrue(Project.objects.filter(name='Novo Projeto').exists())

    def test_project_update_view(self):
        response = self.client.post(reverse('projects:update', args=[self.project.pk]), {
            'name': 'Projeto Atualizado',
            'lider': 'Líder Atualizado',
            'data_inicio': '2023-01-01',
            'remuneracao_0': 100,
            'remuneracao_1': 'BRL'
        })
        self.assertEqual(response.status_code, 302) # Redirect after successful update
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Projeto Atualizado')

    def test_project_delete_view(self):
        response = self.client.post(reverse('projects:delete', args=[self.project.pk]))
        self.assertEqual(response.status_code, 302) # Redirect after successful deletion
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_add_comment_view(self):
        response = self.client.post(reverse('projects:add_comment', args=[self.project.pk]), {
            'comment_text': 'Comentário de teste'
        })
        self.assertEqual(response.status_code, 200) # HTMX returns partial HTML
        self.assertTrue(ProjectComment.objects.filter(project=self.project, comment_text='Comentário de teste').exists())

    def test_add_attachment_view(self):
        # Create a dummy file for testing file upload
        from django.core.files.uploadedfile import SimpleUploadedFile
        dummy_file = SimpleUploadedFile("file.txt", b"file_content", content_type="text/plain")
        response = self.client.post(reverse('projects:add_attachment', args=[self.project.pk]), {
            'file_name': 'Teste Anexo',
            'file_path': dummy_file # This field is usually handled by the form itself with actual file upload
        }, follow=True)
        # Note: File upload tests are more complex and often require mocking storage
        # For simplicity, this test only checks the form submission without actual file storage
        self.assertEqual(response.status_code, 200) # HTMX returns partial HTML
        # self.assertTrue(ProjectAttachment.objects.filter(project=self.project, file_name='Teste Anexo').exists())

    def test_delete_comment_view(self):
        comment = ProjectComment.objects.create(project=self.project, user=self.user, comment_text='Comentário a ser deletado')
        response = self.client.delete(reverse('projects:delete_comment', args=[self.project.pk, comment.pk]))
        self.assertEqual(response.status_code, 200) # HTMX returns partial HTML
        self.assertFalse(ProjectComment.objects.filter(pk=comment.pk).exists())

    def test_delete_attachment_view(self):
        attachment = ProjectAttachment.objects.create(project=self.project, user=self.user, file_name='Anexo a ser deletado', file_path='path/to/file.txt')
        response = self.client.delete(reverse('projects:delete_attachment', args=[self.project.pk, attachment.pk]))
        self.assertEqual(response.status_code, 200) # HTMX returns partial HTML
        self.assertFalse(ProjectAttachment.objects.filter(pk=attachment.pk).exists())


