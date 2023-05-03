import mimetypes
import os

from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .formss import FileForm
from .models import FileTracker, Files


@login_required()
def home_page(request):
    if request.method == 'GET':
        files = Files.objects.all()
        query = ''

    if request.method == "POST":
        query = request.POST.get('q')
        if query:
            files = Files.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:
            files = Files.objects.all()

    return render(request, 'index.html', {'files': files, 'query': query})


def file_preview(request, pk):
    file = get_object_or_404(Files, pk=pk)
    content_type = file.file_type
    file_type = content_type.split('/')[-1]

    if file_type == 'image':
        image_path = file.file.path
        return FileResponse(open(image_path, 'rb'), content_type=content_type)

    elif file_type in ['audio', 'video']:
        return render(request, 'files-preview.html', {'file': file, 'type': file_type})

    else:
        response = HttpResponse(file.file, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{file.title}"'
        return response


def download_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    file_path = file.file.path
    content_type = file.file_type
    file_type = content_type.split('/')[-1]
    filename = f'{file.title}.{file_type}'

    try:
        tracker = file.filetracker
        downloads = tracker.downloads
        tracker.downloads = downloads + 1
        tracker.save()
    finally:
        pass

    response = HttpResponse(open(file_path, 'rb').read(), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename={filename}'
    file_size = os.path.getsize(file_path)
    response['Content-Length'] = file_size

    return response


def send_email_with_attachment(request, pk):
    file = get_object_or_404(Files, pk=pk)
    file_path = file.file.path
    content_type = file.file_type
    file_type = content_type.split('/')[-1]
    filename = f'{file.title}.{file_type}'

    email = EmailMessage(
        subject='Email with Attachment',
        body='Please find the attached file',
        from_email='sethsyd32@gmail.com',
        to=['sethantanah@gmail.com'],
    )
    # Open the file you want to attach
    with open(file_path, 'rb') as f:
        # Add the file as an attachment to the email
        email.attach(filename, f.read(), content_type)
    # Send the email
    email.send()
    try:
        tracker = file.filetracker
        emails = tracker.emails
        tracker.emails = emails + 1
        tracker.save()
    finally:
        pass
    return HttpResponse('Email sent with attachment')


