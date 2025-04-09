from django.urls import path
from . import views

app_name = "maptiles"

urlpatterns = [
    path('dynamic-tile/', views.dynamic_map_tile, name='dynamic_tile'),
]
