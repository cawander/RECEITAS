from django.shortcuts import render


def home(request):
    # return render(request, 'global/home.html')
    return render(request, template_name='recipes/pages/home.html',
                  context={
                      'mensagem': 'Wanderley testando o contexto',
                  }, status=201
                  )


def recipe(request, id):
    # return render(request, 'global/home.html')
    return render(request, template_name='recipes/pages/recipe-view.html',
                  context={
                      'mensagem': 'Wanderley testando o contexto',
                  }, status=201
                  )
