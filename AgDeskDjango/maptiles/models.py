from django.db import models

# Create your models here.
# maptiles/models.py

import uuid
from django.contrib.gis.db import models  # Enable GeoDjango
from django.utils import timezone

class AOI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    geometry = models.PolygonField(srid=4326)  # EPSG:4326 = WGS84
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class SatelliteImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aoi = models.ForeignKey(AOI, on_delete=models.CASCADE, related_name='images')
    satellite_name = models.CharField(max_length=100, default='Sentinel-2')
    tile_id = models.CharField(max_length=100)
    capture_date = models.DateField()
    cloud_cover = models.FloatField()
    image_url = models.URLField()  # Blob link
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('tile_id', 'capture_date')

    def __str__(self):
        return f"{self.tile_id} - {self.capture_date}"


class NDVIMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    satellite_image = models.OneToOneField(SatelliteImage, on_delete=models.CASCADE, related_name='ndvi_map')
    ndvi_raster_url = models.URLField()  # Azure Blob or internal tile server
    ndvi_thumbnail_url = models.URLField(blank=True, null=True)  # Optional preview
    computed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"NDVI for {self.satellite_image}"
