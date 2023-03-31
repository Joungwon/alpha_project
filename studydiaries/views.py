from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'studydiaries/index.html')

def create(request):
    return render(request, 'studydiaries/create.html')