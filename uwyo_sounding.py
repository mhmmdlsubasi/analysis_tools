
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_sounding(day, month, year, time, region, stnm, file_type):
    try:
        link = "http://weather.uwyo.edu/cgi-bin/sounding" 
        day = str(day).zfill(2)
        month = str(month).zfill(2)
        time = str(time).zfill(2)
        params = {
            "region" : region,
            "TYPE" : file_type,
            "YEAR" : year,
            "MONTH" : month,
            "FROM" : day+time,
            "TO" : day+time,
            "STNM" : stnm}
        response = requests.get(link, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        data = soup.find('pre').text
        parametres = soup.find('h3').find_next_sibling('pre').text

        lines = parametres.splitlines()
        del lines[0]

        parametres_dict = {}
        for line in lines:
            parts = line.split(':')
            key = parts[0].strip()
            value = parts[1].strip()
            parametres_dict[key] = value
        return data, parametres_dict
    except:
        print("Bir hata meydana geldi.")
        return [], []

year_input = int(input("Yıl giriniz:\t"))
month_input = int(input("Ay giriniz:\t"))
day_input = int(input("Gün giriniz:\t"))
hour_input = int(input("Saat giriniz (00 veya 12Z):\t") )
stnm_input = int(input("İstasyon numarasını giriniz:\t"))

sondaj = datetime(year_input,month_input,day_input,hour_input)

region = "europe"
file_type = "TEXT:LIST"
stnm = stnm_input
year = sondaj.year
month = sondaj.month
day = sondaj.day
time = sondaj.hour

data, parametres_dict = get_sounding(day, month, year, time, region, stnm, file_type)

print(data)
print(parametres_dict)

