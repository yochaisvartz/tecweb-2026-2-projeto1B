from django.test import TestCase

from .models import Note, Tag


class NoteCrudTests(TestCase):
	def test_create_note(self):
		response = self.client.post(
			'/',
			{'titulo': 'Título novo', 'detalhes': 'Detalhes novos'},
		)

		self.assertRedirects(response, '/')
		self.assertEqual(Note.objects.count(), 1)
		self.assertEqual(Note.objects.get().content, 'Detalhes novos')

	def test_edit_note(self):
		note = Note.objects.create(title='Antigo', content='Conteúdo antigo')

		response = self.client.post(
			f'/notes/{note.id}/edit/',
			{'titulo': 'Atualizado', 'detalhes': 'Conteúdo atualizado'},
		)

		self.assertRedirects(response, '/')
		note.refresh_from_db()
		self.assertEqual(note.title, 'Atualizado')
		self.assertEqual(note.content, 'Conteúdo atualizado')

	def test_delete_note(self):
		note = Note.objects.create(title='Para excluir', content='Conteúdo')

		response = self.client.post(f'/notes/{note.id}/delete/')

		self.assertRedirects(response, '/')
		self.assertFalse(Note.objects.filter(id=note.id).exists())

	def test_get_delete_does_not_remove_note(self):
		note = Note.objects.create(title='Preservada', content='Conteúdo')

		response = self.client.get(f'/notes/{note.id}/delete/')

		self.assertRedirects(response, '/')
		self.assertTrue(Note.objects.filter(id=note.id).exists())

	def test_create_notes_reuses_existing_tag(self):
		first_response = self.client.post(
			'/',
			{'titulo': 'Primeira', 'detalhes': '', 'tag': 'Comida'},
		)
		second_response = self.client.post(
			'/',
			{'titulo': 'Segunda', 'detalhes': '', 'tag': ' comida '},
		)

		self.assertRedirects(first_response, '/')
		self.assertRedirects(second_response, '/')
		self.assertEqual(Tag.objects.filter(name='comida').count(), 1)
		self.assertEqual(Note.objects.filter(tag__name='comida').count(), 2)

	def test_edit_note_can_remove_tag(self):
		tag = Tag.objects.create(name='estudo')
		note = Note.objects.create(title='Anotação', content='', tag=tag)

		response = self.client.post(
			f'/notes/{note.id}/edit/',
			{'titulo': 'Anotação', 'detalhes': '', 'tag': ''},
		)

		self.assertRedirects(response, '/')
		note.refresh_from_db()
		self.assertIsNone(note.tag)

	def test_tag_pages_filter_notes(self):
		tag = Tag.objects.create(name='receitas')
		Note.objects.create(title='Com tag', content='', tag=tag)
		Note.objects.create(title='Sem tag', content='')

		tags_response = self.client.get('/tags/')
		detail_response = self.client.get(f'/tags/{tag.id}/')

		self.assertEqual(tags_response.status_code, 200)
		self.assertEqual(detail_response.status_code, 200)
		self.assertContains(detail_response, 'Com tag')
		self.assertNotContains(detail_response, 'Sem tag')
