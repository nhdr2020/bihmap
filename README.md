# Map of Bosnia Herzegovina
This is the repository for the NHDR 2020 map application. The repository is connected to the `heroku` app at https://bihmap.herokuapp.com/BiH. Whenever a modification is made to this repository, the `heroku` app is automatically recompiled and reloaded. So, please wait a couple of minutes after a modification and reload the app.  

## Files
The top level files `Procfile` and `Requirements.txt` are configuration files for the heroku application. You don't need to modify these files. The code and the data sits in the folder `BiH`.

The file, `BiH/main.py` contains the whole of the code. Basically, this is a `bokeh` application written in `python`. If you do not want to change the behaviour of the application, you do not need to modify the code. Of course, you are welcome to do so if you know what you are doing.

## Data
Usually, you would want to update the data rather than the code.

### Categories
The categories are listed in the file `BiH/data/categories.csv`. The fields are tab separated.

```
category  icon      priority
Airport   airport   30
Bakery    bread     20
Bank      bank_euro	20
```
The name if of the icon file is given in the `icon` column without the extension. There are three priority levels, 10:high, 20:medium and 30:low. If you want to define a new categort, you just need to append a new row to the end of `categories.csv` and create an icon file with file name `new_icon.png` in the folder `BiH/static/symbols/` with an image size `32x37`.

### Points of Interest
The points of interest are listed in the file `BiH/data/point_of_interests.csv`. The fields are semicolumn separated. The field names are self explanatory.
```
category;name;latitude;longitude
Hotel;Jezero Jelah recreational;44.668035;17.966919
Mosque;Mesdžid Samci Salakici;44.693522;17.925577
Mosque;Rafik Hasak's Mosque;44.693094;17.93283
Mosque;Mesdžid Lipe;44.692147;17.943902
```
You can add new rows to this file as long as you provide all the fields and separate them by semicolumns.

## Maps
The maps are in `shape` format. Basically, each `shape` consists of 4 files with the extensions `.dbf`, `.prj`, `.shp` and `.shx`.

The country map is in the folder `BiH/data/country/`. You do not need to modify anything in this folder.

The maps for municipalities are in the folder `BiH/data/municipalities`, each in `shape` format consisting of 4 files.

### Adding new municipalities
If you want to add new municapility (or any administrative region) to the map, you need to generate its `shape` and put it in the folder `BiH/data/municipalities`.

There are several ways to create `shape` files for regions, cities etc. Here is a simple method that does not involve any software setup. It uses freely available web resources. The procedure is described in more detail in https://peteris.rocks/blog/openstreetmap-administrative-boundaries-in-geojson/.

1. Go to https://www.openstreetmap.org/ and search for the administrative unit by its name. Click on the unit link among the search results. It should show you the boundaries of the administrative unit. Copy the `ID` given in the brackets. For example, for Sarajevo, you will see `Relation: City of Sarajevo (2567380)`. Here `2567380` is the `ID`.
2. Go to http://polygons.openstreetmap.fr and paste the `ID` in the field `Id of relation`. Submit. On the results page, click on the `GeoJSON` link and save the file with extension `.geojson`. You need to convert this file to `shape` format in the next and final step.
3. Go to https://mapshaper.org and drop the `.geojson` file that you saved in the previous step into the upper window. Select `import`. It should display an outline of the region map. Export the map, choosing `Shapefile` in the popup. It will save the `shape` as a zip file. Unzip and upload to `BiH/data/municipalities`.
