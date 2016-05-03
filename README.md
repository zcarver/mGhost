# mGhost

Description
-----------
Currently, IndexFungorum(IF), USDA Systematic Mycology and Microbiology Laboratory Fungus-Host Database(SMML) and the Susan C. Tucker Herbarium at Louisiana State University are integrated. This is a 'work-from-directory' script, as such, it should be executed within the working directory. As it is now, mGhost outputs a preliminary csv file containing information queried and a visual of found host specimens that are described with coordinates in Louisiana, USA.

Possible implications of this project include development of meta-information (ecosystem, climatic and geologic histories) for already georeferenced fungal specimens, pathogenic or not, from additional databases to attain a grasp onto the spread of fungal populations.

Installation
------------
The following Python(3) modules are utilized in script:

- Basemap

- Matplotlib

- Numpy

Two dependencies required for the current version of matplotlib/Basemap are:

- cssselect: https://pythonhosted.org/cssselect/

- cycler 0.10.0: https://pypi.python.org/pypi/Cycler

For the complete installation protocol of matplotlib follow: http://matplotlib.org/users/installing.html
and of Basemap: http://matplotlib.org/basemap/users/installing.html
or if using Ubuntu follow: https://peak5390.wordpress.com/2012/12/08/matplotlib-basemap-tutorial-installing-matplotlib-and-basemap/

Usage
-----
Simply the user inputs binomial name of phyto-specific fungal pathogen within double quotes...

:~/Desktop/progproject$ python mycosGeoHost.py --spp "Cercospora flagellaris" --lim 200
 
References
----------
- USDA SMML: http://nt.ars-grin.gov/fungaldatabases/index.cfm
- IndexFungorum: http://www.indexfungorum.org/
- Susan C. Tucker Herbarium: http://data.cyberfloralouisiana.com/lsu/

License
-------
Please refer to license documentation for matplotlib.
