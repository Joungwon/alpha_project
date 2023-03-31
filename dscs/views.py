from django.shortcuts import render,redirect
from .models import Algorithm
from .forms import AlgorithmForm
# Create your views here.
def index(request):
    dscses = Algorithm.objects.all()
    context ={
        'dscses':dscses,
    }
    return render(request, 'dscs/index.html',context)

def create(request):
    
    if request.method =='POST':
        form =AlgorithmForm(request.POST,request.FILES)
        form.save()
        return redirect('dscs:index')
    
    else:
        form = AlgorithmForm()
        context = {
            'form':form
            }
        return render(request,'dscs/create.html',context)

    
def detail(request,pk):
    dscs = pk
    dscs = Algorithm.objects.get(pk=pk) 
    context = {'dscs':dscs,}
    return render(request, 'dscs/detail.html',context)
 