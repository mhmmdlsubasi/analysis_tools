import cdsapi

day_list = []
month_list = []
year_list = []
time_list = []
level_list = []

years = str(input("Çalışma yılını giriniz: (birden fazla ise virgül kulanınız)\n"))
if years =='all': year_list = 'all'
else:
    for year in years.split(","): year_list.append(str(year))

months = str(input("Çalışma ayını giriniz: (birden fazla ise virgül kulanınız)(tüm aylar için 'all' yazınız)\n"))
if months =='all':
    for i in range(1, 13):
        month = str(i).zfill(2)  # "zfill" fonksiyonuyla 1-9 arası sayıların önüne 0 ekliyoruz
        month_list.append(month)
else:
    for month in months.split(","): month_list.append(str(month))

days = str(input("Çalışma gününü giriniz: (birden fazla ise virgül kulanınız)(tüm günler için 'all' yazınız)\n"))
if days =='all':
    for i in range(1, 32):
        day = str(i).zfill(2)  # "zfill" fonksiyonuyla 1-9 arası sayıların önüne 0 ekliyoruz
        day_list.append(day)
else:
    for day in days.split(","): day_list.append(str(day))

times = str(input("Çalışma saatini giriniz: (birden fazla ise virgül kulanınız)(tüm saatler için 'all' yazınız)\n"))
if times =='all':
    for hour in range(0, 24):
        time = f"{hour:02d}:00"
        time_list.append(time)
else:
    for time in times.split(","): time_list.append(str(time))

area_input = str(input('Çalışma alanını seçiniz:\n\t1) Dünya\n\t2) Türkiye\n\t3) Avrupa\n\t4) Koordinat girmek istiyorum\n'))
if area_input == '1': area = [90, -180, -90, 180]
if area_input == '2': area = [36.0, 26.0, 42.0, 45.0]
if area_input == '3': area = [30, -10, 60, 50]
if area_input == '4':
    x1 = input("Başlangıç enlemini giriniz: ")
    x2 = input("Bitiş enlemini giriniz: ")
    y1 = input("Başlangıç boylamını giriniz: ")
    y2 = input("Bitiş boylamını giriniz: ")
    area = [x2,y1,x1,y2]

levels = str(input("Çalışma seviyesini giriniz:\n\t- Yer seviyesi için 0,\n\t- 850hPa seviyesi için 850,\n\t- 800hPa seviyesi için 800,\n\t- 700hPa seviyesi için 700,\n\t- 500hPa seviyesi için 500,\n\t- 300hPa seviyesi için 300,\n\t- 200hPa seviyesi için 200,\n\t- Tamamını çekmek için 9'u tuşlayınız\n"))
if levels =='0': level = '0'
if levels =='9': 
    level = 'upper air'
    level_list = 'all'
else: 
    level = 'upper air'
    for level in levels.split(","): level_list.append(str(level))

grid = '0.1/0.1'


if level == '0': 
    seviye_bilgi = 'single'
    details_1 = f'reanalysis-era5-{seviye_bilgi}-levels'
    details_2 ={
            'product_type': 'reanalysis',
            'variable': [
                '10m_u_component_of_wind',
                '10m_v_component_of_wind',
                '2m_dewpoint_temperature',
                '2m_temperature',
                'mean_sea_level_pressure',
                'mean_wave_direction',
                'mean_wave_period',
                'sea_surface_temperature',
                'significant_height_of_combined_wind_waves_and_swell',
                'surface_pressure',
                'total_precipitation',
            ],
            'year': year_list,
            'month': month_list,
            'day': day_list,
            'time': time_list,
            'area': area,
            'format': 'netcdf',
            'grid': grid,
        }
else: 
    seviye_bilgi = 'pressure'
    details_1 = f'reanalysis-era5-{seviye_bilgi}-levels'
    details_2 ={
            'product_type': 'reanalysis',
            'variable': [
                'divergence', 
                'fraction_of_cloud_cover', 
                'geopotential',
                'ozone_mass_mixing_ratio', 
                'potential_vorticity', 
                'relative_humidity',
                'specific_cloud_ice_water_content', 
                'specific_cloud_liquid_water_content', 
                'specific_humidity',
                'specific_rain_water_content', 
                'specific_snow_water_content', 
                'temperature',
                'u_component_of_wind', 
                'v_component_of_wind', 
                'vertical_velocity',
                'vorticity',
            ],
            'pressure_level': level_list,
            'year': year_list,
            'month': month_list,
            'day': day_list,
            'time': time_list,
            'area': area,
            'format': 'netcdf',
            'grid': grid,
        }

print(details_1)
print(details_2)

def download_era5_data(details_1, details_2):
    c = cdsapi.Client()
    c.retrieve(details_1, details_2, 'era5_data.nc')  # Verilerin kaydedileceği dosya adı

download_era5_data(details_1, details_2)
