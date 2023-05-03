from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from library.formss import FileForm
from library.models import FileTracker

from library.models import Files


@permission_required('user.can_add_files', raise_exception=True)
def dashboard(request):
    files = FileTracker.objects.all()
    paginator = Paginator(files, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    file_count = FileTracker.objects.count()
    categories = [
        'Pdf',
        'Audio',
        'Video',
        'Images'
    ]

    data = {'categories': categories, 'count': file_count}
    return render(request, 'dashboard.html', {'page_obj': page_obj, 'data': data, 'files': files})


def search_files(request):
    query = request.GET.get('q')
    if query:
        results = Files.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results = []
    return render(request, 'search-results.html', {'query': query, 'results': results})


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
