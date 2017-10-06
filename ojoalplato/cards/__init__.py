# Uses projected coordinate system for Spain.
# See: https://epsg.io/2062
DEFAULT_PROJECTED_SRID = 2062
DEFAULT_WGS84_SRID = 4326
DEFAULT_GOOGLE_MAPS_SRID = 3857

WINE_KIND_CHOICES = (
    ("white", "Blanco"),
    ("red", "Tinto"),
    ("rose", "Rosado"),
)

DAY_CHOICES = (
    (0, "Lunes"),
    (1, "Martes"),
    (2, "Miércoles"),
    (3, "Jueves"),
    (4, "Viernes"),
    (5, "Sábado"),
    (6, "Domingo")
)
