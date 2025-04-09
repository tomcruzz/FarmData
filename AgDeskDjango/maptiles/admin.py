from django.contrib import admin
from .models import AOI, SatelliteImage, NDVIMap


# Register your models here.

@admin.register(AOI)
class AOIAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(SatelliteImage)
class SatelliteImageAdmin(admin.ModelAdmin):
    list_display = ('tile_id', 'aoi', 'capture_date', 'cloud_cover')
    list_filter = ('capture_date', 'satellite_name')

@admin.register(NDVIMap)
class NDVIMapAdmin(admin.ModelAdmin):
    list_display = ('satellite_image', 'computed_at')
