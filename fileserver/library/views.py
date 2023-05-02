import mimetypes
import os

from django.http import FileResponse, HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required


from .formss import FileForm
from .models import FileTracker, Files


@login_required()
def home_page(request):
    files = Files.objects.all()
    return render(request, 'index.html', {'files': files})


def file_preview(request, pk):
    file = get_object_or_404(Files, pk=pk)

    if file.file_type == 'pdf':
        response = HttpResponse(file.file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.title}"'
        return response

    elif file.file_type in ['audio', 'video']:
        return render(request, 'files-preview.html', {'file': file})

    else:
        image_path = file.file.path
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')


def download_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    filename = file.title
    file_path = file.file.path
    try:
        tracker = file.filetracker
        downloads = tracker.downloads
        tracker.downloads = downloads + 1
        tracker.save()
    finally:
        pass

    if file.file_type == 'pdf':
        content_type = 'application/pdf'
        filename = f'{file.title}.{file.file_type}'



    elif file.file_type == 'audio':
        content_type = 'audio/mpeg'
        filename = f'{file.title}.mp3'

    elif file.file_type == 'video':
        content_type = 'video/mp4'
        filename = f'{file.title}.mp4'

    else:
        content_type = 'image/jpeg'
        filename = f'{file.title}.jpeg'

    response = HttpResponse(open(file_path, 'rb').read(), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={filename}'
    file_size = os.path.getsize(file_path)
    response['Content-Length'] = file_size

    return response


@permission_required('user.can_add_files', raise_exception=True)
def add_file(request):
    if request.method == 'GET':
        form = FileForm()
        return render(request, 'add-file.html', {'form': form})
    if request.method == 'POST':
        form = FileForm(request.POST)

        if form.is_valid():
            file = form.save()
            file_tracker = FileTracker()
            file_tracker.file = file
            file_tracker.save()

            return redirect(reverse('index'))
        else:
            return render(request, 'add-file.html', {'form': form})
