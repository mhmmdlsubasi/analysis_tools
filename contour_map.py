import xarray as xr  # xarray kütüphanesini "xr" takma adıyla içe aktarın
import matplotlib.pyplot as plt  # matplotlib.pyplot kütüphanesini "plt" takma adıyla içe aktarın
import cartopy.crs as ccrs  # cartopy.crs kütüphanesini "ccrs" takma adıyla içe aktarın
from datetime import datetime  # datetime modülünden datetime sınıfını içe aktarın
from cartopy.feature import NaturalEarthFeature  # cartopy.feature kütüphanesinden NaturalEarthFeature sınıfını içe aktarın
import cartopy.feature as cfeature  # cartopy.feature kütüphanesini "cfeature" takma adıyla içe aktarın
import numpy as np  # numpy kütüphanesini "np" takma adıyla içe aktarın
import os

# Veri setini "era5_data.nc" dosyasından yükleyin
data = xr.open_dataset('era5_data.nc')

def draw_map(p_level, i):
    # Yeni bir grafik figürü oluşturun ve boyutunu belirleyin
    plt.figure(figsize=(25, 15))
    # Projeksiyon olarak "PlateCarree"yi kullanarak bir eksen oluşturun
    ax = plt.axes(projection=ccrs.PlateCarree())

    # İl sınırlarını temsil eden veri setini yükleyin
    provinces = NaturalEarthFeature(category='cultural',
                                    name='admin_1_states_provinces_lines',
                                    scale='10m',
                                    facecolor='none',
                                    edgecolor='black',
                                    linestyle='--')
    ax.add_feature(provinces, linestyle='--', edgecolor='gray', linewidth=0.5)

    # Kıyı çizgilerini çizin
    ax.coastlines(resolution='10m', linewidths=0.75)
    # Sınırları çizin
    ax.add_feature(cfeature.BORDERS, linewidths=0.75)
    # Enlem ve boylamları göster
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=1, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    # gl.xformatter = gridliner.LongitudeFormatter()
    # gl.yformatter = gridliner.LatitudeFormatter()

    # Enlem ve boylam sembollerini ekle
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlocator = plt.FixedLocator(np.arange(22, 46, 2))
    gl.ylocator = plt.FixedLocator(np.arange(30, 48, 2))
    gl.xlabel_style = {'size': 12, 'color': 'black'}
    gl.ylabel_style = {'size': 12, 'color': 'black'}
    
    # Ankara'nın enlem ve boylam değerlerini tanımlayın
    ankara_latitude = 39.9334
    ankara_longitude = 32.8597
    # Ankara'nın bulunduğu noktaya bir nokta çizin
    ax.plot(ankara_longitude, ankara_latitude, 'ko', markersize=5, transform=ccrs.PlateCarree())
    # Ankara yazısını eksen üzerinde belirtilen konuma ekleyin
    ax.text(ankara_longitude - 1, ankara_latitude, 'Ankara', transform=ccrs.PlateCarree(), fontsize=13, va='bottom')

    # EĞRİ CONTOUR
    # egri_var değişkeninin contour grafiğini çizin
    contour_1 = egri_var.plot.contour(ax=ax, levels=np.arange(0, egri_var.values.max(), 6), colors='k', linewidths=3)
    # Kontur etiketlerini ekle
    plt.clabel(contour_1, inline=True, fontsize=15, fmt='%.1f')

    # RENK CONTOUR
    # renk_var değişkeninin renkli kontur grafiğini çizin
    contour_2 = renk_var.plot.contourf(ax=ax, levels=np.arange(0, 100, 1), cmap='jet', extend='both', add_colorbar=False)
    # Renk skalasını oluşturun ve ekle
    cbar = plt.colorbar(contour_2, ax=ax, orientation='horizontal', pad=0.0225, aspect=50)
    cbar.set_label('Bağıl Nem (%)', fontsize=24, fontweight='bold')
    cbar.ax.tick_params(labelsize=22)

    # Oklar arasındaki mesafeleri belirleyin
    barb_spacing_x = 18  # x eksenindeki oklar arasındaki mesafe
    barb_spacing_y = 18  # y eksenindeki oklar arasındaki mesafe
    # Rüzgar oklarını çizin
    ax.barbs(
        data['longitude'].values[::barb_spacing_x],
        data['latitude'].values[::barb_spacing_y],
        u.values[::barb_spacing_y, ::barb_spacing_x],
        v.values[::barb_spacing_y, ::barb_spacing_x],
    )
    # Grafik başlıklarını ayarlayın
    plt.title('', loc='center')
    plt.title(f'{p_level}hPa Jeopotansiyel Yükseklik, Bağıl Nem ve Rüzgar Haritası', loc='left', fontsize=24,
              fontweight='bold')
    plt.title(f'{formatted_time}', loc='right', fontsize=24, fontweight='bold')

    # Ek bilgileri eksen üzerine ekleyin
    plt.text(0.99, 0.075, 'Muhammed Ali Subaşı\nAli Çalışkan', transform=ax.transAxes, ha='right', va='top',
             fontsize=20, zorder=10,
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
    plt.text(0.99, 0.98, 'Veri: ERA5', transform=ax.transAxes, ha='right', va='top', fontsize=20, zorder=10,
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

    # Grafiği sıkıştırın ve kaydedin
    plt.tight_layout()
    path = f"output/{p_level}/z_r_wind/"
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(path+f"{formatted_time}.png", dpi=300)
    print(path+f"'{formatted_time}.png' completed.")
    plt.close()

# Basınç seviyelerini ve zamanları döngülerle dolaşarak grafikleri oluşturun
p_levels = [850, 700, 500, 300, 200]
for p_level in p_levels:
    for i in range(0, 72): # 0'dan 72'ye kadar dönen bir döngü oluşturuyoruz (zaman indeksi)
        # Zaman değerini alın
        time_value = (data["time"][i].values)
        time_value = str(time_value)
        parsed_time = datetime.strptime(time_value[0:-7], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = parsed_time.strftime("%d %B %Y %HZ")

        # Sıcaklık değerlerini alın ve birimleri dönüştürün
        temp = data['t'].sel(level=p_level)[i, :, :]
        temp -= 273.15

        # Yükseklik değerlerini alın ve birimleri dönüştürün
        geo = data['z'].sel(level=p_level)[i, :, :]
        geo /= 100.0

        # Rüzgar bileşenlerini alın ve birimleri dönüştürün
        u = data['u'].sel(level=p_level)[i, :, :]
        u *= 1.9438444924

        v = data['v'].sel(level=p_level)[i, :, :]
        v *= 1.9438444924

        # Bağıl nem değerlerini alın
        # humidity = data['r'].sel(level=p_level)[i, :, :]

        # Diğer değişkenleri isteğe bağlı olarak alabilirsiniz

        # Renkli kontur grafiği için kullanılacak değişkenleri belirleyin
        renk_var = temp
        egri_var = geo

        # graph fonksiyonunu çağırarak grafiği oluşturun
        draw_map(p_level, i)
