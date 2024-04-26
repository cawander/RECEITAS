from django.shortcuts import render


def view_home(request):
    # return render(request, 'global/home.html')
    return render(request, template_name='recipes/pages/home.html',
                  context={
                      'mensagem': 'Wanderley testando o contexto',
                  }, status=201
                  )
