import xarray as xr  # xarray kütüphanesini xr olarak içe aktarıyoruz
import pandas as pd  # pandas kütüphanesini pd olarak içe aktarıyoruz

data = xr.open_dataset("era5_data.nc")  # "era5_data.nc" dosyasını xarray ile açıp data değişkenine atıyoruz

sozluk = {"time": data["time"].values}  # "time" değişkenini sozluk sözlüğüne ekliyoruz
for i in data:  # data üzerinde döngü oluşturuyoruz
    sozluk.setdefault(f"{i}", data[f"{i}"][:, 2, 0, 0].values)  # her bir değişken için ilgili indekslere sahip değerleri sozluk sözlüğüne ekliyoruz

dataset = pd.DataFrame(sozluk)  # sozluk sözlüğünü pandas DataFrame'e dönüştürüyoruz ve dataset değişkenine atıyoruz
dataset.to_csv("veri.csv", index=False)  # dataset'i "veri.csv" dosyasına CSV formatında kaydediyoruz (indeksleri kaydetmiyoruz)