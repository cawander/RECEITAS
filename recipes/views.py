from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
# from utils.recipes.factory import make_recipe
from .models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')

    return render(request, template_name='recipes/pages/home.html',
                  context={'recipes': recipes})


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    return render(request, template_name='recipes/pages/category.html',
                  context={
                      'recipes': recipes,
                      'title': f'{recipes[0].category.name} - Category | ',
                  }
                  )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(
        request,
        template_name='recipes/pages/recipe-view.html',
        context={
            'recipe': recipe,
            'is_detail_page': True,
        }
    )


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(
                description__icontains=search_term),
        ),
        is_published=True,
    ).order_by('-id')

    return render(
        request,
        template_name='recipes/pages/search.html',
        context={
            'page_title': f'Search for  "{search_term}"',
            'search_term': search_term,
            'recipes': recipes,
        },
    )
