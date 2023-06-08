import os

from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from library.formss import FileForm
from library.models import FileTracker
from library.models import Files
from accounts.models import User






config = {
    'apiKey': "AIzaSyBS2xUVtdq9RvsyhQrzSSuyaQVPbIYA95Y",
    'authDomain': "home-status-c4316.firebaseapp.com",
    'projectId': "home-status-c4316",
    'storageBucket': "home-status-c4316.appspot.com",
    'messagingSenderId': "1083784871321",
    'appId': "1:1083784871321:web:f86f3181602153fc562708",
    'measurementId': "G-MEBSQ6SJGV",
    "databaseURL": ""
}

# firebase = pyrebase.initialize_app(config)
# auth = firebase.auth()
# storage = firebase.storage()


def save_image(file):


    return ''
    # if auth.current_user is not None:
    #     storage.child("files/" + file.name).put(file)
    #     return storage.child("files/" + file.name).get_url(auth.current_user['idToken'])
    # else:
    #     user = auth.sign_in_with_email_and_password('sethsyd32@gmail.com', os.environ.get('EMAIL_PASSWORD'))
    #     storage.child("files/" + file.name).put(file)
    #     return storage.child("files/" + file.name).get_url(user['idToken'])





@permission_required('user.can_add_files', raise_exception=True)
def dashboard(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        if query:
            files = FileTracker.objects.filter(Q(file__title__icontains=query) | Q(file__description__icontains=query))
        else:
            files = FileTracker.objects.all()

    if request.method == 'GET':
        query = ''
        files = FileTracker.objects.all()

    paginator = Paginator(files, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    file_count = FileTracker.objects.count()
    users_count = User.objects.count()
    users = User.objects.all()
    categories = [
        'Pdf',
        'Audio',
        'Video',
        'Images'
    ]

    data = {'categories': categories, 'count': file_count, 'users_count': users_count}
    return render(request, 'dashboard.html', {'page_obj': page_obj, 'users': users, 'data': data, 'query': query})


@permission_required('user.can_add_files', raise_exception=True)
def upload_file(request):
    if request.method == 'GET':
        form = FileForm()
        return render(request, 'add-file.html', {'form': form})
    if request.method == 'POST':
        form = FileForm(request.POST)

        if form.is_valid():
            file = form.save(commit=False)
            file.file = request.FILES['file']
            file.file_url = save_image(request.FILES['file'])
            file_tracker = FileTracker()
            file_tracker.file = file
            file.save()
            file_tracker.save()
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'add-file.html', {'form': form})


@permission_required('user.can_add_files', raise_exception=True)
def update_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    if request.method == 'GET':
        form = FileForm(instance=file)
        return render(request, 'update-file.html', {'form': form})

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'update-file.html', {'form': form})


@permission_required('user_can_delete_file', raise_exception=True)
def delete_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    return render(request, 'delete-file.html', {'file': file})


@permission_required('user_can_delete_file', raise_exception=True)
def confirm_delete_file(request, pk):
    file = get_object_or_404(Files, pk=pk)
    file.delete()
    return redirect(reverse('dashboard'))
