Ocean Data Grapher
==================
The Ocean Data Grapher library contains python programs to assist in developing
graphs for handling netcCDF data from NOAAs OOI net portal

Usage
-----
### Climatology Mapping ###
__Basic Format__
```
python3 ClimatologyMap.py -f <filepath>
```
__Specifying Time Ranges__
```
python3 ClimatologyMap.py -f <file> -i <start_date>:<end_date>
python3 ClimatologyMap.py -f path_to_file.nc -i 2019-09-05:2019-09-14
python3 ClimatologyMap.py -f path_to_file.nc -i 2019-09:2019-10
```
By specifying an interval that you're interested in graphing you can cut away
any extra unwanted data. _start_date_ and _end_date_ are of datetime format.
You can be as specific or unspecific as you want as long as they are of the
same time precision. eg. You cant have 2019-09:2019-09-07T21
__Specifying Precision__
```
python3 ClimatologyMap.py -f <filepath> -p [Y|M|D|h]
```
Specifying precision allows you to graph in chunks of a year(Y), month(M),
day(D), or hour(h). Keep in mind that the more segmented your graph the longer
it will take to parse.
