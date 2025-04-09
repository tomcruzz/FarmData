# maptiles/urls.py

from django.urls import path
from . import views

app_name = "maptiles"

urlpatterns = [
    path('dynamic-tile/', views.dynamic_map_tile, name='dynamic_tile'),
    
    # Base dashboard map
    path('dashboard/', views.map_dashboard_view, name='map_dashboard'),

    # HTMX partial loader
    path('ndvi/<uuid:aoi_id>/', views.ndvi_htmx_view, name='ndvi_htmx_view'),

    # Full NDVI page
    path('ndvi-page/<uuid:aoi_id>/', views.ndvi_page_view, name='ndvi_page_view'),

    path('aoi-geojson/<uuid:aoi_id>/', views.aoi_geojson, name='aoi_geojson'),

    path('ndvi-stream/<uuid:aoi_id>/', views.ndvi_stream, name='ndvi_stream'),

    # Local NDVI tile cache serving
    path("ndvi-tile/<date>/<z>/<x>/<y>.jpg", views.cached_ndvi_tile, name="cached_ndvi_tile"),

    path("cached-tile/<str:date>/<str:z>/<str:x>/<str:y>.jpg", views.cached_ndvi_tile, name="cached_ndvi_tile"),


]
