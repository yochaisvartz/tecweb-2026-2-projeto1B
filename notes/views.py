from django.shortcuts import get_object_or_404, render, redirect
from .models import Note, Tag


def get_tags(tags_string):
    seen_names = []
    for raw_name in tags_string.split(','):
        normalized_name = raw_name.strip().lower()
        if normalized_name and normalized_name not in seen_names:
            seen_names.append(normalized_name)

    return [Tag.objects.get_or_create(name=name)[0] for name in seen_names]


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.create(title=title, content=content)
        note.tags.set(get_tags(request.POST.get('tag', '')))
        return redirect('index')
    else:
        all_notes = Note.objects.prefetch_related('tags').all()
        tags = Tag.objects.order_by('name')
        return render(request, 'notes/index.html', {'notes': all_notes, 'tags': tags})


def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.save()
        note.tags.set(get_tags(request.POST.get('tag', '')))
        return redirect('index')

    tag_value = ', '.join(note.tags.order_by('name').values_list('name', flat=True))
    return render(request, 'notes/edit.html', {'note': note, 'tag_value': tag_value})


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
    notes = tag.notes.prefetch_related('tags')
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})