import base64
import io
from unittest.mock import patch

from PIL import Image

from ojoalplato.cards.templatetags.card_tags import osm_static_map


def _tile_response(request, timeout):
    tile = Image.new("RGB", (256, 256), (40, 120, 80))
    data = io.BytesIO()
    tile.save(data, "PNG")
    return io.BytesIO(data.getvalue())


@patch("ojoalplato.cards.templatetags.card_tags.urllib.request.urlopen", _tile_response)
def test_osm_static_map_fills_canvas_and_centers_marker():
    from ojoalplato.cards.templatetags.card_tags import fetch_osm_tile

    fetch_osm_tile.cache_clear()
    result = osm_static_map((2.1734, 41.3851), 235, 201, 13)

    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[1])))

    assert image.size == (235, 201)
    assert image.getpixel((0, 0)) == (40, 120, 80)
    assert image.getpixel((117, 100))[0] > 150


@patch("ojoalplato.cards.templatetags.card_tags.urllib.request.urlopen", side_effect=OSError)
def test_osm_static_map_returns_empty_when_tiles_are_unavailable(urlopen):
    from ojoalplato.cards.templatetags.card_tags import fetch_osm_tile

    fetch_osm_tile.cache_clear()
    assert osm_static_map((2.1734, 41.3851), 235, 201, 13) == ""
