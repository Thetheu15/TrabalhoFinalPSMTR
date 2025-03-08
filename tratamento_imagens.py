import pydicom
import cv2
import os
import numpy as np

# Caminho da pasta contendo os arquivos DICOM
caminho_arquivo = "Data/I1352658"

# Listar todos os arquivos DICOM da pasta
imagens = [
    os.path.join(caminho_arquivo, f)
    for f in os.listdir(caminho_arquivo)
    if f.endswith(".dcm")
]

count = 0
# Exibir as imagens e metadados usando OpenCV
for image_path in imagens:
    dicom_image = pydicom.dcmread(image_path)
    pixel_array = dicom_image.pixel_array

    # Normalizar os valores de pixel para a faixa 0-255
    pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
    pixel_array = np.uint8(pixel_array)  # Converter para uint8

    # Exibir metadados importantes
    print(f"\nImagem {count+1}: {image_path}")
    print(f"  - Dimensões: {pixel_array.shape}")
    print(f"  - Tipo de aquisição: {dicom_image.SeriesDescription}")
    
    # Tentar extrair b-values e direções de difusão
    if hasattr(dicom_image, "DiffusionBValue"):
        print(f"  - B-Value: {dicom_image.DiffusionBValue}")
    if hasattr(dicom_image, "DiffusionGradientOrientation"):
        print(f"  - Gradiente de difusão: {dicom_image.DiffusionGradientOrientation}")

    # Exibir a imagem
    cv2.imshow("Imagem DICOM", pixel_array)
    
    # Aguarda tecla para exibir a próxima imagem
    cv2.waitKey(0)
    
    if count == 10:  # Limite de imagens a serem exibidas
        break
    count += 1

# Fechar todas as janelas
cv2.destroyAllWindows()