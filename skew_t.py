from datetime import datetime  # datetime modülünden datetime sınıfını içe aktarıyoruz
import xarray as xr  # xarray kütüphanesini xr olarak içe aktarıyoruz
import matplotlib.pyplot as plt  # matplotlib.pyplot modülünü plt olarak içe aktarıyoruz
from metpy.plots import SkewT  # metpy.plots modülünden SkewT sınıfını içe aktarıyoruz
from metpy.units import units  # metpy.units modülünden units sınıfını içe aktarıyoruz
import numpy as np  # numpy kütüphanesini np olarak içe aktarıyoruz

data = xr.open_dataset("era5_data.nc")  # "era5_data.nc" dosyasını xarray ile açıp data değişkenine atıyoruz

station = 'Ankara'  # İstasyon adını belirtiyoruz

for i in range(0, 4):  # 0'dan 4'e kadar dönen bir döngü oluşturuyoruz (zaman indeksi)
    # Zaman değerini al
    time_value = (data["time"][i].values)  # Zaman değerini data değişkeninden alıyoruz
    time_value = str(time_value)  # Zaman değerini stringe dönüştürüyoruz
    parsed_time = datetime.strptime(time_value[0:-7], "%Y-%m-%dT%H:%M:%S.%f")  # Zamanı uygun formata dönüştürüyoruz
    dt = parsed_time.strftime("%d %B %Y %HZ")  # Formatlı zamanı dt değişkenine atıyoruz

    # Gerekli verileri al

    p = data["level"]  # Basınç değerlerini p değişkenine atıyoruz
    r = data["r"][i, :, 2, 26]  # Nem değerlerini r değişkenine atıyoruz
    T = data["t"][i, :, 2, 26] - 273.15  # Sıcaklık değerlerini T değişkenine atıyoruz ve Kelvin'i Celsius'a dönüştürüyoruz
    u = data["u"][i, :, 2, 26]  # Uçak hızı değerlerini u değişkenine atıyoruz
    v = data["v"][i, :, 2, 26]  # Uçak yönü değerlerini v değişkenine atıyoruz

    N = (np.log(r / 100) + ((17.27 * T) / (237.3 + T))) / 17.27  # Nem oranını hesaplayan formülü kullanarak N değerini elde ediyoruz
    D = (237.3 * N) / (1 - N)  # Çiy noktasını hesaplayan formülü kullanarak D değerini elde ediyoruz

    Td = D  # Çiy noktası değerini Td değişkenine atıyoruz

    # Skew-T çizimi için gerekli ayarlamalar

    fig = plt.figure(figsize=(9, 11))  # Çizim figürünü oluşturuyoruz ve boyutunu ayarlıyoruz
    skew = SkewT(fig, rotation=45)  # SkewT çizimi için SkewT sınıfını kullanarak bir nesne oluşturuyoruz

    # Verileri çiz

    skew.plot(p, T, 'r')  # Sıcaklık eğrisini çiziyoruz (kırmızı renkte)
    skew.plot(p, Td, 'g')  # Çiy noktası eğrisini çiziyoruz (yeşil renkte)
    skew.plot_barbs(p[::3], u[::3], v[::3], y_clip_radius=0.03)  # Rüzgar oklarını çiziyoruz

    skew.ax.set_xlim(-30, 40)  # x ekseni sınırlarını ayarlıyoruz
    skew.ax.set_ylim(1020, 100)  # y ekseni sınırlarını ayarlıyoruz

    # Özel çizgileri ekle

    skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K, alpha=0.25, color='orangered')  # Kuru adiyabatları çiziyoruz (turuncu-kırmızı renkte)
    skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K, alpha=0.25, color='tab:green')  # Nemli adiyabatları çiziyoruz (yeşil renkte)

    # Açıklamaları ekle

    plt.title('{} Sounding'.format(station), loc='left')  # Başlığa istasyon adını ekliyoruz (sol tarafa)
    plt.title('Valid Time: {}'.format(dt), loc='right')  # Başlığa geçerli zamanı ekliyoruz (sağ tarafa)

    plt.savefig(f"{dt}.png", dpi=300)  # Oluşturulan çıktıyı "dt.png" adıyla kaydediyoruz (dpi değeri 300 olarak ayarlanmış)
