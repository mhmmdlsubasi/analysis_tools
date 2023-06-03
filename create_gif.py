import imageio
import os

# Görüntülerin dosya adlarını bir listede toplayın
path = 'C:/Users/Administrator/Desktop/resized/'

# 'address' dizinindeki her 'p_level_folder' için döngü oluşturun
for p_level_folder in os.listdir(path):
    # Her 'p_level_folder' içindeki her 'map_type' için döngü oluşturun
    for map_type in os.listdir(path + p_level_folder + "/"):
        image_files = []
        
        # 'p_level_folder' ve 'map_type' altındaki dosyaları listeleyin ve 'image_files' listesine ekleyin
        for file in os.listdir(path + p_level_folder + "/" + map_type):
            image_files.append(file)

        # Görüntüleri açın
        images = [imageio.imread(path + p_level_folder + "/" + map_type + "/" + file) for file in image_files]

        # 'gif' dizini yoksa oluşturun
        if not os.path.exists(f'gif/{p_level_folder}/'):
            os.makedirs(f'gif/{p_level_folder}/')

        # GIF'i oluşturun ve kaydedin
        imageio.mimsave(f'gif/{p_level_folder}/{map_type}.gif', images, duration=0.5, loop=0)