from django.http import Http404
from django.http import JsonResponse
from django.db.models import Q  # , F, Value
from django.db.models.aggregates import Count  # Sum, Max, Min, Avg, ...
# from django.db.models.functions import Concat
from django.forms.models import model_to_dict
# from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import gettext as _
# from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from utils.recipes.pagination import make_pagination
from tag.models import Tag

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))
QTY_PAGES = int(os.environ.get('QTY_PAGES', 8))

# https://docs.djangoproject.com/pt-br/4.0/ref/models/querysets/#field-lookups
# https://docs.djangoproject.com/pt-br/4.0/ref/models/querysets/#operators-that-return-new-querysets


def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.filter(
    #     #     id=F('author__id'),
    #     # ).order_by('-id', 'title')[:1]
    #     Q(
    #         Q(title__icontains='da',
    #           id__gt=2,
    #           is_published=True,) |
    #         Q(
    #             id__gt=1000
    #         )
    #     )
    # )[:10]
    # recipes = Recipe.objects.values('id', 'title')[:5]
    # recipes = Recipe.objects.all().annotate(
    #     author_full_name=Concat(
    #         F('author__first_name'), Value(' '),
    #         F('author__last_name'), Value(' ('),
    #         F('author__username'), Value(')'),
    #     )
    # )
    recipes = Recipe.objects.get_published()
    number_of_recipes = recipes.aggregate(number=Count('id'))

    context = {
        # 'recipes': recipes
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
    }

    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category', 'author__profile')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
                'html_language': html_language,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - '
            f'{category_translation} | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')
        ).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
