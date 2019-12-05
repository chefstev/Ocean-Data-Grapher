import numpy as np
import sys
import glob
import xarray as xr
from datetime import datetime
from netCDF4 import Dataset
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Blues4

# Current thought for the graph is the date/temp max-min actual,average and then the average line over it

paths = glob.glob('PC01A-CTD/deployment0006_RS01SBPS-PC01A-4A-CTDPFA103-streamed-ctdpf_optode_sample_20190902T000000.501132-20191106T000132.022397.nc')
dataset = xr.open_mfdataset(paths)

# Get the time variable to be set as a dimension and coordinate that we can use to index our data by the date it
# was recieved
dataset.coords['time'] = ('time', dataset.time)

# Create a new dataarray that will store the seawater_temperature in time dimension
da_seawater_temp = xr.DataArray(dataset.seawater_temperature, dims=['time'], coords={'time': dataset.time})

# =====Slicing for testing speed purposes======
#da_seawater_temp = da_seawater_temp.sel(time='2019-09-02')

# Get the date for the first entry
# If we want to change precision just change the [<unit>] to something else
start_date = da_seawater_temp.time.values[0].astype('datetime64[D]')
# Get the date of the last entry
end_date = da_seawater_temp.time.values[-1].astype('datetime64[D]')
end_date_string = np.datetime_as_string(end_date)
# Difference between them
timedelta = end_date-start_date
timedelta_int = timedelta.astype(int) + 1
# Array containing each date
dates = []

# Datastructure maps from datetime64 to average temperature over that time
average_temp_map = {}
# Datastructure maps from datetime64 to min temperature over that time
min_temp_map = {}
# Datastructure maps from datetime64 to max temperature over that time
max_temp_map = {}

# Temperature measurements array
average_temp = []
min_temp = []
max_temp = []

def progress(date_string, final_date, number, total):
    delta = number / float(total)
    total_progress = '=' * int(delta * 10)
    progress_image = '\rGetting data for date: %s last_date: %s |%s> %s %%' % (date_string, final_date, total_progress, int(delta * 100))
    print(progress_image, end='')

curr_date = start_date
count = 1
while not curr_date > end_date:
    dates.append(curr_date)
    date_string = np.datetime_as_string(curr_date)
    progress(date_string, end_date_string, count, timedelta_int)
    try: # Missing data for date
        da_seawater_temp_slice = da_seawater_temp.sel(time=date_string)
    except:
        continue
    average = da_seawater_temp_slice.mean().item()
    min = da_seawater_temp_slice.min().item()
    max = da_seawater_temp_slice.max().item()
    average_temp_map[curr_date] = average
    average_temp.append(average)
    min_temp_map[curr_date] = min
    min_temp.append(min)
    max_temp_map[curr_date] = max
    max_temp.append(max)
    curr_date += 1
    count += 1

# Close off the progress bar
print()
print("==Finshed organizing data==")

source = ColumnDataSource(data={
    'time_left'                 : np.asarray(dates),
    'time_right'                : np.asarray(dates) + 1,
    'seawater_temp_average'     : average_temp,
    'seawater_temp_min'         : min_temp,
    'seawater_temp_max'         : max_temp
})

plot = figure(title="Seawater Temperature vs Time (PC01A CTD)", x_axis_type="datetime", plot_width=800)
plot.xaxis.axis_label = 'Date'
plot.yaxis.axis_label = 'Temperature (Celcius)'

tooltips = [
    ('Seawater Temperature Average', '@seawater_temp_average'),
    ('Date', '@time_left{%F}')
]
formatters = {
    'time_left': 'datetime'
}

plot.line(x='time_left', y='seawater_temp_average', line_width=2, color=Blues4[0], source=source)
plot.quad(top='seawater_temp_max', bottom='seawater_temp_min', left='time_left', right='time_right',
    color=Blues4[2], alpha=0.5, source=source)

plot.add_tools(HoverTool(tooltips=tooltips, formatters=formatters))
show(plot)
