from django.shortcuts import render
import csv

def get_data_from_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data
# Create your views here.
def index(request):
    return render(request,'scraps/index.html')
# def crud(request):
#     file_path = 'data.csv'
#     data = get_data_from_csv(file_path)
#     context = {'data': data}
#     return render(request, 'index.html', context)
def crud(request):
    return render(request,'scraps/html.html')
