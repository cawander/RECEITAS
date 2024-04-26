from django.urls import path

from recipes.views import view_home


urlpatterns = [
    path('', view_home),
]
