from django.shortcuts import render, get_object_or_404
from .models import AOI
from django.http import JsonResponse
from django.core.serializers import serialize
import json
# For real-time NDVI stream
import time
from django.http import StreamingHttpResponse
import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import reverse


def dynamic_map_tile(request):
    date = request.GET.get('date')
    tile_url = f"/media/tiles/{date}/tile.png"  # Adjust this path based on where your tiles live
    return render(request, 'maptiles/map_tile_snippet.html', {'tile_url': tile_url})



def ndvi_htmx_view(request, aoi_id):
    aoi = get_object_or_404(AOI, id=aoi_id)
    selected_date = request.GET.get("ndviDate", "2021-01-01")

    # Use internal Django tile proxy route (cached)
    ndvi_url = f"https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/{selected_date}/3857/{{z}}/{{y}}/{{x}}.jpg"


    context = {
        "aoi": aoi,
        "ndvi_url": ndvi_url
    }

    return render(request, "maptiles/partials/ndvi_map.html", context)



def ndvi_page_view(request, aoi_id):
    aoi = get_object_or_404(AOI, id=aoi_id)

    # Pass this to both views
    ndvi_url = "https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/2021-01-01/3857/{z}/{y}/{x}.jpg"

    return render(request, "maptiles/ndvi_page.html", {
        "aoi": aoi,
        "ndvi_url": ndvi_url 
    })



def map_dashboard_view(request):
    return render(request, 'maptiles/map_tile_snippet.html')



def aoi_geojson(request, aoi_id):  # <-- include `aoi_id` to match the URL
    aoi = get_object_or_404(AOI, id=aoi_id)
    geojson = serialize('geojson', [aoi], geometry_field='geometry', fields=('id', 'name'))
    parsed_geojson = json.loads(geojson)  
    return JsonResponse(parsed_geojson)



def ndvi_stream(request, aoi_id):
    def event_stream():
        while True:
            time.sleep(5)  # replace this with backend condition later
            yield f"data: New NDVI update available\n\n"
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')



def cached_ndvi_tile(request, date, z, x, y):
    tile_path = os.path.join(
        settings.MEDIA_ROOT,
        "ndvi-cache",
        date,
        z,
        x,
        f"{y}.jpg"
    )
    if os.path.exists(tile_path):
        return FileResponse(open(tile_path, "rb"), content_type="image/jpeg")
    else:
        raise Http404("Tile not found in cache.")
