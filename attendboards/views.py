from django.shortcuts import render, redirect
from .forms import AttendanceForm
from .models import Attendance
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def write(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('attendboards:index')
    else:
        form = AttendanceForm()

    context = {'form': form}
    return render(request, 'attendboards/write.html', context)

def index(request):
    articles = Attendance.objects.all()
    context = {'articles': articles}
    return render(request, 'attendboards/index.html', context)