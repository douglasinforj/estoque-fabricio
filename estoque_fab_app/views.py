from django.shortcuts import render

def home(request):
    return render(request, 'estoque_fab_app/home.html')