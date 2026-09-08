from django.shortcuts import get_object_or_404, render, redirect
from .models import Note, Tag


def get_tag(tag_name):
    normalized_name = tag_name.strip().lower()
    if not normalized_name:
        return None

    tag, _ = Tag.objects.get_or_create(name=normalized_name)
    return tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = get_tag(request.POST.get('tag', ''))
        Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')
    else:
        all_notes = Note.objects.select_related('tag').all()
        tags = Tag.objects.order_by('name')
        return render(request, 'notes/index.html', {'notes': all_notes, 'tags': tags})


def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.tag = get_tag(request.POST.get('tag', ''))
        note.save()
        return redirect('index')

    return render(request, 'notes/edit.html', {'note': note})


def delete(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        note.delete()

    return redirect('index')


def tags(request):
    all_tags = Tag.objects.order_by('name')
    return render(request, 'notes/tags.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    notes = Note.objects.filter(tag=tag).select_related('tag')
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})