from django.shortcuts import render

def dynamic_map_tile(request):
    date = request.GET.get('date')
    tile_url = f"/media/tiles/{date}/tile.png"  # Adjust this path based on where your tiles live
    return render(request, 'maptiles/map_tile_snippet.html', {'tile_url': tile_url})
