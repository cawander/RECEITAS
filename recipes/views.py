from django.shortcuts import render

from utils.recipes.factory import make_recipe


def home(request):
    # return render(request, 'global/home.html')
    return render(request, template_name='recipes/pages/home.html',
                  context={
                      'recipes': [make_recipe() for _ in range(10)],
                  }, status=201
                  )


def recipe(request, id):
    # return render(request, 'global/home.html')
    return render(request, template_name='recipes/pages/recipe-view.html',
                  context={
                      'recipe': make_recipe(),
                      'is_detail_page': True,
                  }, status=201
                  )
