# osm_scripts

## Pre-render desired regions
Extract desired regions(polygons) from http://geojson.io/ 
    and copy down the generated geojson into the `polygons.json`.
Then run `generate_meta2tile.py` script. It will generate `tiles.txt` file.
Now you have to run below command to render you regions tiles(see https://www.volkerschatz.com/net/osm/render_list.html for more details):

`cat tiles.txt | render_list -m YOUR_MAP_NAME -f -n 20`



## Extract  mbtiles
If you want to extract mbtiles file, just run this command(see https://github.com/geofabrik/meta2tile):

`meta2tile --mbtiles /var/lib/mod_tile/YOUR_MAP_NAME targetfile`


   
   