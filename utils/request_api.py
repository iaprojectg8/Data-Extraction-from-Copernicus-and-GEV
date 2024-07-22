import time

FILE_FORMAT = "netcdf"
EXTENSION = "nc"


# Make a false request, just to dev the app
def make_false_request(year):
    print(year)
    time.sleep(4)

# This does not work because of the different month size
def make_day_request(lat,lon,year,month,day,dataset,param,c,input_folder,resolution=0.25):
    lat_max=lat+resolution
    lon_min=lon-resolution
    lat_min=lat-resolution
    lon_max=lon+resolution
    if dataset=='reanalysis-era5-pressure-levels':
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'pressure_level': '1000',
                'year': year,
                'month': month,
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  day,
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}-{month}-{day}.{EXTENSION}')
    else :
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'year': year,
                'month': month,
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  day,
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}-{month}-{day}.{EXTENSION}')

# After some tests, this is longer to execute than the year request     
def make_month_request(lat,lon,year,month,dataset,param,c,input_folder,resolution=0.25):
    lat_max=lat+resolution
    lon_min=lon-resolution
    lat_min=lat-resolution
    lon_max=lon+resolution

    # For the ERA5 single level dataset
    if dataset == 'reanalysis-era5-single-levels':
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'year': year,
                'month': month,
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  [f'{day:02d}' for day in range(1, 32)],
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}-{month}.{EXTENSION}')
        
    # For the ERA5 pressure level dataset
    elif dataset=='reanalysis-era5-pressure-levels':
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'pressure_level': '1000',
                'year': year,
                'month': month,
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  [f'{day:02d}' for day in range(1, 32)],
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}-{month}.{EXTENSION}')
    
    # For the WFDE5 dataset
    elif dataset == "derived-near-surface-meteorological-variables":
        resolution = resolution*2
        lat_max=lat+resolution
        lon_min=lon-resolution
        lat_min=lat-resolution
        lon_max=lon+resolution
        c.retrieve(
        dataset,
        {
            'product_type': 'reanalysis',
            'format': 'zip',
            'variable': param,
            'reference_dataset': 'cru',
            'year': year,
            'month': month,
            'time': [f'{hour:02d}:00' for hour in range(24)],
            'day':  [f'{day:02d}' for day in range(1, 32)],
            'area': [
                lat_max,lon_min,lat_min,lon_max
            ],
            'version': '2.1',
        },
        f'{input_folder}/{year}-{month}.zip')

# Should be the better but the time for each request is always different
def make_year_request(lat,lon,year,dataset,param,c,input_folder,resolution=0.25):
    lat_max=lat+resolution
    lon_min=lon-resolution
    lat_min=lat-resolution
    lon_max=lon+resolution

    # For the ERA5 single level dataset
    if dataset == 'reanalysis-era5-single-levels':
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'year': year,
                'month': [f'{month:02d}' for month in range(1, 13)],
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  [f'{day:02d}' for day in range(1, 32)],
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}.{EXTENSION}')
    
    # For the ERA5 pressure level dataset
    elif dataset=='reanalysis-era5-pressure-levels':
        c.retrieve(
            dataset,
            {
                'product_type': 'reanalysis',
                'format': FILE_FORMAT,
                'variable': param,
                'pressure_level': '1000',
                'year': year,
                'month': [f'{month:02d}' for month in range(1, 13)],
                'time': [f'{hour:02d}:00' for hour in range(24)],
                'day':  [f'{day:02d}' for day in range(1, 32)],
                'area': [
                    lat_max,lon_min,lat_min,lon_max
                ],
            },
            f'{input_folder}/{year}.{EXTENSION}')
    
    # For the WFDE5 dataset, but not useful because of the limit given by the Climate Data Store 
    elif dataset == "derived-near-surface-meteorological-variables":
        resolution = resolution*2
        lat_max=lat+resolution
        lon_min=lon-resolution
        lat_min=lat-resolution
        lon_max=lon+resolution
        c.retrieve(
        dataset,
        {
            'product_type': 'reanalysis',
            'format': 'zip',
            'variable': param,
            'reference_dataset': 'cru',
            'year': year,
            'month': [f'{month:02d}' for month in range(1, 13)],
            'time': [f'{hour:02d}:00' for hour in range(24)],
            'day':  [f'{day:02d}' for day in range(1, 32)],
            'area': [
                lat_max,lon_min,lat_min,lon_max
            ],
            'version': '2.1',
        },
        f'{input_folder}/{year}.zip')

        