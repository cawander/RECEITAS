from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest import skip


# @skip('A mensagem do porquê estou pulando esses testes.')
class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:home')
        )
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_templates(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    @skip('WIP - Work in progress')
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:home')
        )
        self.assertIn(
            '<h1> No recipe found 😢</h1>',
            response.content.decode('utf-8')
        )

        # Tenho que escrever mais algumas coisas sobre este teste
        # self.fail('para que eu termine de digitá-lo.')

    def test_recipe_home_templates_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:home')
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        # Check if one recipe exists
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""

        # Need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1> No recipe found 😢</h1>',
            response.content.decode('utf-8')
        )
