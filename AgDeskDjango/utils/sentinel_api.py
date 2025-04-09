# utils/sentinel_api.py

import os
import json
import requests
from datetime import datetime, timedelta
from django.core.files.base import ContentFile
from maptiles.models import AOI, NDVIMap

# Load .env
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("SENTINEL_CLIENT_ID")
CLIENT_SECRET = os.getenv("SENTINEL_CLIENT_SECRET")
INSTANCE_ID = os.getenv("SENTINEL_INSTANCE_ID")

AUTH_URL = "https://services.sentinel-hub.com/oauth/token"
PROCESS_URL = "https://services.sentinel-hub.com/api/v1/process"

def get_access_token():
    res = requests.post(AUTH_URL, json={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    })
    res.raise_for_status()
    return res.json()["access_token"]

def fetch_ndvi_for_aoi(aoi_id):
    aoi = AOI.objects.get(pk=aoi_id)
    polygon = json.loads(aoi.geometry.geojson)  # GeoJSON format
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    evalscript = """
    //VERSION=3
    function setup() {
        return {
            input: ["B08", "B04"],
            output: {
                bands: 1,
                sampleType: "FLOAT32"
            }
        };
    }

    function evaluatePixel(sample) {
        let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
        return [ndvi];
    }
    """

    payload = {
        "input": {
            "bounds": {
                "geometry": polygon
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": (datetime.utcnow() - timedelta(days=15)).isoformat() + "Z",
                        "to": datetime.utcnow().isoformat() + "Z"
                    }
                }
            }]
        },
        "output": {
            "width": 512,
            "height": 512,
            "responses": [{
                "identifier": "default",
                "format": {
                    "type": "image/png"
                }
            }]
        },
        "evalscript": evalscript
    }

    response = requests.post(PROCESS_URL, headers=headers, json=payload)
    response.raise_for_status()

    ndvi_file = ContentFile(response.content)
    filename = f"ndvi_{aoi.name}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.png"

    ndvi_map = NDVIMap(
        aoi=aoi,
        date=datetime.utcnow()
    )
    ndvi_map.image.save(filename, ndvi_file)
    ndvi_map.save()
    print(f"✅ NDVI Map saved: {filename}")
