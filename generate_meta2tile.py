import geopandas as gpd
from shapely.geometry.polygon import Polygon

import math


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)


def generate_poly_tiles(poly: Polygon, out):
    bbox = poly.envelope
    tiles = {}
    for z in range(0, 19):
        tiles[z] = set()

        tile_xs = []
        tile_ys = []
        for i in range(0, 4):
            x = bbox.boundary.xy[0][i]
            y = bbox.boundary.xy[1][i]
            tile_x, tile_y = deg2num(y, x, z)
            tile_xs.append(tile_x)
            tile_ys.append(tile_y)
        min_tile_x, min_tile_y = (min(tile_xs), min(tile_ys))
        max_tile_x, max_tile_y = (max(tile_xs), max(tile_ys))

        for tile_x in range(min_tile_x - 1, max_tile_x + 1):
            for tile_y in range(min_tile_y - 1, max_tile_y + 1):
                nw = num2deg(tile_x, tile_y, z)
                sw = num2deg(tile_x, tile_y + 1, z)
                ne = num2deg(tile_x + 1, tile_y, z)
                se = num2deg(tile_x + 1, tile_y + 1, z)
                box = Polygon([nw, sw, se, sw, nw])
                if box.intersects(poly):
                    tiles[z].add((tile_x, tile_y))

    for z in tiles:
        for (x, y) in tiles[z]:
            out.write('{0} {1} {2}\n'.format(x, y, z))

    out.write('0 0 0\n')


data = gpd.read_file("polygons.json")

with open('tiles.txt', 'w') as out:
    for index, row in data.iterrows():
        poly = row['geometry']
        generate_poly_tiles(poly, out)
