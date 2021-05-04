# Map of Bosnia Herzegovina

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

## Points of Interest
The points of interest are listed in the file `BiH/data/point_of_interests.csv`. The fields are semicolumn separated. The field names are self explanatory.
```
category;name;latitude;longitude
Hotel;Jezero Jelah recreational;44.668035;17.966919
Mosque;Mesdžid Samci Salakici;44.693522;17.925577
Mosque;Rafik Hasak's Mosque;44.693094;17.93283
Mosque;Mesdžid Lipe;44.692147;17.943902
```
