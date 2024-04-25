from django.shortcuts import render
from django.http import HttpResponse


def view_home(request):
    # return render(request, 'global/home.html')
    return render(request, 'recipes/home.html')


# def view_home(request):
#   return HttpResponse('Home')


def view_sobre(request):
    return HttpResponse('Sobre')


def view_contato(request):
    return HttpResponse('Contato')
