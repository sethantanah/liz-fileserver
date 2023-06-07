import mimetypes
import os

from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .formss import FileForm
from .models import FileTracker, Files


def home_page(request, *args, **kwargs):
    empty_query = False
    shared = request.session.get('shared', False)
    download = request.session.get('download', False)
    if request.method == 'GET':
        files = Files.objects.all()
        query = ''

    if request.method == "POST":
        query = request.POST.get('q')
        if query:
            files = Files.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        else:
            files = Files.objects.all()
            if len(files) == 0:
                empty_query = True

    if shared:
        request.session['shared'] = False

    if download:
        request.session['download'] = False

    return render(request, 'index.html', {'files': files, 'query': query, 'shared': shared, 'download': download, 'empty_query': empty_query})


@login_required()
def file_preview(request, pk):
    file = get_object_or_404(Files, pk=pk)
    content_type = file.file_type
    file_type = content_type.split('/')[-1]


    if file_type == 'pdf':
        response = HttpResponse(file.file, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{file.title}"'
        return response

    else:
        response = HttpResponse(file.file, content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{file.title}"'
        return render(request, 'files-preview.html', {'file': file, 'type': file_type})


@login_required()
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
    request.session['downloaded'] = True
    return response


@login_required()
def send_email_with_attachment(request, pk):
    file = get_object_or_404(Files, pk=pk)
    file_path = file.file.path
    content_type = file.file_type
    file_type = content_type.split('/')[-1]
    filename = f'{file.title}.{file_type}'
    my_mail = request.user.email
    email = EmailMessage(
        subject='Lizz-fileserver',
        body='Please find the attached file',
        from_email='sethsyd32@gmail.com',
        to=[my_mail],
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
    request.session['shared'] = True
    return redirect(reverse('index'))


def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


