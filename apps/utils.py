from PIL import Image
from io import BytesIO


# def optimize_image(image):
#     """Optimiza una imagen y devuelve un objeto de imagen optimizada."""
#     with BytesIO() as f:
#         # Guardamos la imagen en memoria
#         image.save(f, format='JPEG', optimize=True)
#         # Cargamos la imagen optimizada desde memoria
#         optimized_image = Image.open(f)
#
#     return optimized_image


# def optimize_image(image):
#     """Optimiza una imagen y devuelve un objeto de imagen optimizada."""
#     optimized_image = Image.open(image)
#     # Redimenciona la imágen si es más grande que 800 píxeles en el lado más largo
#     if optimized_image.height > 800 or optimized_image.width > 800:
#         output_size = (800, 800)
#         optimized_image.thumbnail(output_size)
#         optimized_image.save(image, optimize=True, quality=75)
#
#     return optimized_image



def optimize_image(imagen_path):
    """Optimiza una imagen dada"""
    img = Image.open(imagen_path)
    # Redimensiona la imagen si es más grande que 800 píxeles en el lado más largo
    if img.height > 800 or img.width > 800:
        output_size = (800, 800)
        img.thumbnail(output_size)

        # Si la imagen está en modo RGBA, conviértela a modo RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Crea un buffer temporal para almacenar la imagen optimizada
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', optimize=True, quality=85)
        buffer.seek(0)

        # Guarda la imagen optimizada en el archivo original
        with open(imagen_path, 'wb') as f:
            f.write(buffer.read())
