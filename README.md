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
