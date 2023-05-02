from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView

from .formss import FileForm
from .models import FileTracker, Files


@login_required()
def home_page(request):
    return render(request, 'index.html')


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





