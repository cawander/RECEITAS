from django.urls import path

from recipes.views import view_home, view_contato, view_sobre


urlpatterns = [
    path('', view_home),
    path('sobre/', view_sobre),
    path('contato/', view_contato),
]
